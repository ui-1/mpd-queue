import os
import time
from beets.plugins import BeetsPlugin
from mpd import MPDClient


class MPDQueuePlugin(BeetsPlugin):

    def __init__(self):
        super(MPDQueuePlugin, self).__init__()
        self.register_listener('after_write', self.gather_imported_files)
        self.register_listener('import', self.queue)
        self.paths = set()

    def gather_imported_files(self, item):
        songpath = item.destination().decode('utf-8')
        songpath = os.path.relpath(songpath, '/home/user/Beets')  # TODO: read from conf
        self.paths.add(songpath)

    def queue(self, lib, paths):
        client = MPDClient()
        client.connect('localhost', 6600, 5)  # TODO: read from conf

        client.update()
        print('Updating MPD database…')
        time.sleep(3)

        for path in sorted(self.paths):
            print(f'Adding to MPD queue: {path}')
            client.add(path)
