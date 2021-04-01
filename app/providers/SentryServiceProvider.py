"""A SentryServiceProvider Service Provider."""

from masonite.provider import ServiceProvider
from ..hooks.sentry import SentryHook


class SentryServiceProvider(ServiceProvider):
    """Provides Services To The Service Container."""

    wsgi = False

    def register(self):
        """Register objects into the Service Container."""
        self.app.bind('SentryExceptionHook', SentryHook())

    def boot(self):
        """Boots services required by the container."""
        pass
