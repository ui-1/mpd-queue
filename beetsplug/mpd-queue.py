import time
from beets.plugins import BeetsPlugin
from mpd import MPDClient


class MPDQueuePlugin(BeetsPlugin):

    def __init__(self):
        super(MPDQueuePlugin, self).__init__()
        self.register_listener('album_imported', self.gather_imported_files)
        self.register_listener('import', self.queue)
        self.paths = set()

    def gather_imported_files(self, album):
        for item in album.items():
            songpath = item.destination(fragment=True)
            self.paths.add(songpath)

    def queue(self, lib, paths):
        client = MPDClient()
        host = self.config['host'].get()
        port = self.config['port'].get()
        client.connect(host, port)

        client.update()
        print('Updating MPD database…')
        time.sleep(3)

        for path in sorted(self.paths):
            print(f'Adding to MPD queue: {path}')
            client.add(path)
