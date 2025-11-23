from requests import Session

class SessionModel:
    def __init__(self):
        self.session = Session()

    def newSession(self):
        self.session = Session()

    def getSession(self):
        return self.session

    def setCookies(self, cookies):
        self.session.cookies = cookies
    def getCookies(self):
        return self.session.cookies

    def setHeaders(self, headers):
        self.session.headers = headers
    def getHeaders(self):
        return self.session.headers