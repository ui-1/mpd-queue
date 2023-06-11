import confuse.exceptions
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

    def queue(self):
        client = MPDClient()

        try: port = self.config['port'].get()
        except confuse.exceptions.NotFoundError: port = 6600

        try: host = self.config['host'].get()
        except confuse.exceptions.NotFoundError: host = 'localhost'

        client.connect(host, port)
        client.update()

        for path in sorted(self.paths):
            client.add(path)
