"""Map Local addons"""

import json
from pickle import TRUE
from mitmproxy import http
import logging

from urllib.parse import urlparse, urljoin
from urllib.parse import parse_qs

from mitmproxy.addonmanager import Loader
from mitmproxy.log import ALERT
logger = logging.getLogger(__name__)
import time

class MapLocalConfig:
    def __init__(self, url, method, mapLocalFile, status_code = 200):
        self.url = url
        self.method = method
        self.mapLocalFile = mapLocalFile
        self.status_code = status_code

class QuanMapLocal:
    def __init__(self):
        self.loadConfigs()

    def request(self, flow: http.HTTPFlow):
        self.loadConfigs()
        for config in self.mapLocalConfigs:
            if self.isSameURL(config.url, flow.request.pretty_url) == True and config.method == flow.request.method and config.mapLocalFile is not None:
                fp= open("local-files/{0}".format(config.mapLocalFile), "r")
                data = fp.read()
                fp.close()
                time.sleep(1)
                flow.response = http.Response.make(
                    config.status_code,  # (optional) status code
                    data,  # (optional) content
                    {"Content-Type": "application/json"},  # (optional) headers
                    )
                
    def loadConfigs(self):
        fp= open("config.json", "r")
        data = json.load(fp)
        mapLocalConfigs = []
        for config in data:
            mapLocalConfig = MapLocalConfig(config["url"], config["method"], config["local_file"], config["status_code"])
            mapLocalConfigs.append(mapLocalConfig)
        fp.close()

        self.mapLocalConfigs = mapLocalConfigs

    def isSameURL(self, lhs, rhs) -> bool:
        parsed_lhs = urlparse(lhs)
        lhsQueryParams = parse_qs(parsed_lhs.query)
        parsed_rhs = urlparse(rhs)
        rhsQueryParams = parse_qs(parsed_rhs.query)

        lshURL = urljoin(lhs, parsed_lhs.path)
        rshURL = urljoin(lhs, parsed_rhs.path)

        lhsKeys = list(lhsQueryParams.keys())
        rhsKeys = list(rhsQueryParams.keys())

        if lshURL != rshURL:
            return False
        
        if len(lhsKeys) != len(rhsKeys):
            return False
        
        for key in lhsKeys:
            if lhsQueryParams[key] != rhsQueryParams[key]:
                return False
            
        for key in rhsKeys:
            if lhsQueryParams[key] != rhsQueryParams[key]:
                return False
            
        return True
        


addons = [QuanMapLocal()]