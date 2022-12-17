from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import http.server
import socketserver
import json
import time
from pathlib import Path




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

performActions()
