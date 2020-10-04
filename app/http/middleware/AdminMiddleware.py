"""Admin Middleware."""

from masonite.request import Request


class AdminMiddleware:
    """Admin Middleware."""

    def __init__(self, request: Request):
        """Inject Any Dependencies From The Service Container.

        Arguments:
            Request {masonite.request.Request} -- The Masonite request object
        """
        self.request = request

    def before(self):
        """Run This Middleware Before The Route Executes."""
        try:
            if self.request.user().role == None:
                self.request.redirect('/main')
        except AttributeError:
            self.request.redirect('/main')

    def after(self):
        """Run This Middleware After The Route Executes."""
        pass
