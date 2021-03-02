"""A RestartWebserverJob Queue Job."""

from masonite.queues import Queueable
from tools.server.restart_server import restart_server


class RestartWebserverJob(Queueable):
    """A RestartWebserverJob Job."""

    def __init__(self):
        """A RestartWebserverJob Constructor."""
        pass

    def handle(self):
        """Logic to handle the job."""
        restart_server()
