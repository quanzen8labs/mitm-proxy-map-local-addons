"""Map Local addons"""

import json
from mitmproxy import http
import logging

from mitmproxy.addonmanager import Loader
from mitmproxy.log import ALERT
logger = logging.getLogger(__name__)


class MapLocalConfig:
    def __init__(self, url, method, mapLocalFile):
        self.url = url
        self.method = method
        self.mapLocalFile = mapLocalFile

class QuanMapLocal:
    def __init__(self):
        self.loadConfigs()

    def request(self, flow: http.HTTPFlow):
        self.loadConfigs()
        for config in self.mapLocalConfigs:
            if config.url == flow.request.pretty_url and config.method == flow.request.method and config.mapLocalFile is not None:
                fp= open("local-files/{0}".format(config.mapLocalFile), "r")
                data = fp.read()
                fp.close()
                flow.response = http.Response.make(
                    200,  # (optional) status code
                    data,  # (optional) content
                    {"Content-Type": "application/json"},  # (optional) headers
                    )
                
    def loadConfigs(self):
        fp= open("config.json", "r")
        data = json.load(fp)
        mapLocalConfigs = []
        for config in data:
            mapLocalConfig = MapLocalConfig(config["url"], config["method"], config["local_file"])
            mapLocalConfigs.append(mapLocalConfig)
        fp.close()

        self.mapLocalConfigs = mapLocalConfigs

addons = [QuanMapLocal()]