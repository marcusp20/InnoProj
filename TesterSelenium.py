from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import http.server
import socketserver
import json
import time
from pathlib import Path

filename = 'sites.txt'


class Action:
    def __init__(self, action_type, xpath, value):
        self.action_type = action_type
        self.xpath = xpath
        self.value = value

    def __str__(self):
        return f"type: {self.action_type}, xpath: {self.xpath}, value: {self.value}"


class Site:
    def __init__(self, url, actions):
        self.url = url
        self.actions = actions


def default(o):
    if isinstance(o, Action):
        return {
            'action_type': o.action_type,
            'xpath': o.xpath,
            'value': o.value
        }
    elif isinstance(o, Site):
        obj = {
            "url": o.url,
            "actions": []
        }
        for a in o.actions:
            obj["actions"].append({
                'action_type': a.action_type,
                'xpath': a.xpath,
                'value': a.value
            })
        return obj
    else:
        raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


def write_to_file(sites):
    # Open the file in write mode
    with open(filename, 'w') as f:
        # Convert the sites list to a JSON string
        data = json.dumps(sites, default=default)
        # Write the JSON string to the file
        f.write(data)


def object_hook(d):
    if 'actions' in d:
        return Site(d['url'], [Action(a['action_type'], a['xpath'], a['value']) for a in d['actions']])
    return d


# Read the sites and actions from a text file
def read_from_file():
    myfile = Path(filename)
    myfile.touch(exist_ok=True)

    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read the contents of the file
        data = f.read()
        if data == '':
            return []

        # Convert the JSON string to a list of sites
        sites = json.loads(data, object_hook=object_hook)
        return sites


class MyServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        self.send_response(200)

    def do_POST(self):
        # Read the request body
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        # Unpack the JSON object from the request body
        data = json.loads(body)

        print(data)

        sites = read_from_file()

        foundSite = False
        for s in sites:
            if (s.url == data["site"]):
                foundSite = True
                lastAction = s.actions[len(s.actions) - 1]
                if (data["action_type"] == "keypress" and lastAction.action_type == "keypress" and lastAction.xpath ==
                        data["xpath"]):
                    lastAction.value = lastAction.value + data["value"]
                else:
                    s.actions.append(Action(action_type=data["action_type"], xpath=data["xpath"], value=data["value"]))

                break

        if foundSite is False:
            newSite = Site(url=data["site"],
                           actions=[Action(action_type=data["action_type"], xpath=data["xpath"], value=data["value"])])
            sites.append(newSite)

        write_to_file(sites)

        # Send a response
        self.send_response(200)
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(MyServer, self).end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


def launchServerForPersistence():
    my_server = None
    handler_object = MyServer
    PORT = 8000
    print(f'Starting: http://localhost:{PORT}')
    try:
        socketserver.TCPServer.allow_reuse_address = True  # solution for `OSError: [Errno 98] Address already in use`
        my_server = socketserver.TCPServer(("", PORT), handler_object)
        my_server.serve_forever()
    except KeyboardInterrupt:
        # solution for `OSError: [Errno 98] Address already in use - when stoped by Ctr+C
        print('Stoped by "Ctrl+C"')
    finally:
        # solution for `OSError: [Errno 98] Address already in use
        print('Closing')
        if my_server is not None:
            my_server.server_close()


def parseActions(actionsJson):
    jsonObjs = []
    if type(actionsJson) == str:
        jsonObjs = json.loads(actionsJson)

    events = []
    for action in jsonObjs:
        events.append(Action(action["action_type"], action["xpath"], action["value"]))
    return events


def performActions():
    events = parseActions(
        "[{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/header[1]/div[2]/a[1]\",\"value\":\"\"},"
        "{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/header[1]/div[4]/div[2]/div[1]/div[1]/a[1]\","
        "\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div["
        "1]/div[1]/div[1]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div["
        "1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[@id=\\\"date\\\"]\",\"value\":\"\"},"
        "{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div["
        "1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr["
        "3]/td[3]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div["
        "1]/div[1]/div[2]/div[2]/ul[1]/li[2]/div[1]/div[1]/div[3]/a[1]\",\"value\":\"\"},{\"type\":\"click\","
        "\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/div[2]/div[1]/button["
        "2]/svg[1]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div["
        "1]/div[1]/ul[1]/li[1]/div[2]/div[1]/button[2]/svg[1]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body["
        "1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div[2]/button[1]/span[1]\",\"value\":\"\"}]")

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.billet.dk/")
    driver.implicitly_wait(10)

    for e in events:
        element = driver.find_element(By.XPATH, e.xpath)
        actionChain = ActionChains(driver)
        actionChain.move_to_element(element)
        if e.action_type == "click":
            actionChain.click(element)
        else:
            element.send_keys(e.value)

        actionChain.perform()


def recordSiteTemplate(URL):
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(URL)

    with open('trackSnippet.js', 'r') as file:
        trackSnippet = file.read()

    trackSnippet = trackSnippet.replace('\n', '')

    alive = True
    while alive:
        driver.execute_script(trackSnippet)
        time.sleep(1)
        # Check if the browser is still open.
        try:
            url = driver.current_url
        except WebDriverException:
            alive = False


# recordSiteTemplate("https://www.billetlugen.dk/")
launchServerForPersistence()
# performActions()
