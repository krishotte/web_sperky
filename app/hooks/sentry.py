from raven import Client
from os import environ

client = Client(environ['SENTRY_CONN'])


class SentryHook:
    def __init__(self):
        pass

    def load(self, app):
        # self._app = app
        client.captureException()
