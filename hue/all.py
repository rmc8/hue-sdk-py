class All:
    def __init__(self, parent):
        self.base: str = parent.base
        self.request = parent.request
    
    def lights(self):
        return self.request(path="lights")
    
    def groups(self):
        return self.request(path="groups")
    
    def schedules(self):
        return self.request(path="schedules")
    
    def scenes(self):
        return self.request(path="scenes")
    
    def sensors(self):
        return self.request(path="sensors")
    
    def rules(self):
        return self.request(path="rules")
    
    def timezones(self):
        return self.request(path="timezones")
    
    def resourcelinks(self):
        return self.request(path="resourcelinks")
    
    def capabilities(self):
        return self.request(path="capabilities")
