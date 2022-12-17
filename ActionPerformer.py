import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from SiteAndActionClasses import Action, Site
from ActionRecorder import read_from_file
import json


def parseActions(actionsJson):
    jsonObjs = []
    if type(actionsJson) == str:
        jsonObjs = json.loads(actionsJson)

    events = []
    for action in jsonObjs:
        events.append(Action(action["action_type"], action["xpath"], action["value"]))
    return events


def performActions():
    # events = parseActions(
    #     "[{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/header[1]/div[2]/a[1]\",\"value\":\"\"},"
    #     "{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/header[1]/div[4]/div[2]/div[1]/div[1]/a[1]\","
    #     "\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div["
    #     "1]/div[1]/div[1]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div["
    #     "1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[@id=\\\"date\\\"]\",\"value\":\"\"},"
    #     "{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div["
    #     "1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr["
    #     "3]/td[3]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div["
    #     "1]/div[1]/div[2]/div[2]/ul[1]/li[2]/div[1]/div[1]/div[3]/a[1]\",\"value\":\"\"},{\"type\":\"click\","
    #     "\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/div[2]/div[1]/button["
    #     "2]/svg[1]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body[1]/div[1]/div[2]/div[2]/main[1]/div[1]/div["
    #     "1]/div[1]/ul[1]/li[1]/div[2]/div[1]/button[2]/svg[1]\",\"value\":\"\"},{\"type\":\"click\",\"xpath\":\"/body["
    #     "1]/div[1]/div[2]/div[2]/main[1]/div[1]/div[1]/div[2]/button[1]/span[1]\",\"value\":\"\"}]")

    sites = read_from_file("demo.txt")
    site1 = sites[0]

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(site1.url)
    driver.implicitly_wait(10)

    try:
        for e in site1.actions:
            element = driver.find_element(By.XPATH, e.xpath)
            actionChain = ActionChains(driver)
            actionChain.move_to_element(element)
            if e.action_type == "click":
                actionChain.click(element)
            else:
                element.send_keys(e.value)

            actionChain.perform()
    # If it encounters an element it can't find, it'll
    except selenium.common.exceptions.NoSuchElementException:
        print("Can't take you further than this.")

    alive = True
    while alive:
        time.sleep(10)
        try:
            url = driver.current_url
        except selenium.WebDriverException:
            alive = False

if __name__ == "__main__":
    performActions()
