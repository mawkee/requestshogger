import datetime
import os
from functools import lru_cache

import cherrypy
import tinydb

ROOTDIR = os.path.dirname(os.path.abspath(__file__))


class RequestStorage:
    def __init__(self):
        if "HOGGER_PERSIST" in os.environ:
            self.storage = tinydb.TinyDB("hogger.json")
        else:
            self.storage = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)

    def clean(self):
        self.storage.purge()

    def push(self, item):
        self.storage.insert(item)

    def delete(self, idx):
        self.storage.remove(doc_ids=[idx])

    @property
    def items(self):
        return self.storage.all()


class Greedo:
    def __init__(self, storage):
        self.request_storage = storage

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def default(self, *args, **kwargs):
        data = {
            "datetime": str(datetime.datetime.now()),
            "method": cherrypy.request.method,
            "path": "/".join(cherrypy.request.args),
            "headers": cherrypy.request.headers,
            "params": " | ".join(
                [f"{k}={v}" for k, v in cherrypy.request.params.items()]
            ),
        }

        self.request_storage.push(data)
        return data


class App:
    def __init__(self, storage):
        self.request_storage = storage

    @lru_cache(maxsize=2)
    def get_main_page(self):
        fname = os.path.join(ROOTDIR, "static", "html", "main.html")
        with open(fname, "r") as fsock:
            page = fsock.read()
        return page

    @cherrypy.expose
    def index(self):
        return self.get_main_page()

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def data(self, *args, **kwargs):
        return {
            "data": [
                {"idx": item.doc_id, **item} for item in self.request_storage.items
            ]
        }

    @cherrypy.expose
    def clean(self):
        """Clean the requests list."""
        self.request_storage.clean()
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def delete(self, idx):
        self.request_storage.delete(int(idx))
        raise cherrypy.HTTPRedirect("/")


if __name__ == "__main__":
    host = os.environ.get("HOGGER_HOST", "127.0.0.1")
    port = int(os.environ.get("HOGGER_PORT", 8910))
    config = {
        "global": {
            "server.socket_host": host,
            "server.socket_port": port,
            "server.thread_pool": 4,
        },
    }
    static_conf = {
        "/": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(ROOTDIR, "static"),
        }
    }

    storage = RequestStorage()

    cherrypy.tree.mount(Greedo(storage), "/hog")
    cherrypy.tree.mount(App(storage), "/")
    cherrypy.tree.mount(None, "/static", config=static_conf)
    cherrypy.config.update(config)

    cherrypy.engine.start()
    cherrypy.engine.block()
