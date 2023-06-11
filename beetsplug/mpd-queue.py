import os
import time
import confuse.exceptions
from beets.plugins import BeetsPlugin
from beets import config
from mpd import MPDClient


class MPDQueuePlugin(BeetsPlugin):

    def __init__(self):
        super(MPDQueuePlugin, self).__init__()
        self.register_listener('item_copied', self.gather_imported_files)
        self.register_listener('import', self.queue)
        self.paths = set()
        self.client = MPDClient()

    def gather_imported_files(self, destination):
        fullpath = destination.decode('utf-8')
        base = os.path.expanduser(str(config['directory']))
        relpath = os.path.relpath(fullpath, base)
        self.paths.add(relpath)

    def block_until_update_finishes(self):
        """MPDClient's update method only tells the MPD server to "start updating the database" without actually
        waiting for it to finish. Trying to add a newly imported song to the queue before it's in the database results
        in an exception, so we poll the client's status until the update *has* finished.
        """
        while True:
            if 'updating_db' in self.client.status():
                time.sleep(0.1)
            else:
                return

    def queue(self):

        try: port = self.config['port'].get()
        except confuse.exceptions.NotFoundError: port = 6600

        try: host = self.config['host'].get()
        except confuse.exceptions.NotFoundError: host = 'localhost'

        self.client.connect(host, port)
        self.client.update()
        self.block_until_update_finishes()

        for path in sorted(self.paths):
            self.client.add(path)
