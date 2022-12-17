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