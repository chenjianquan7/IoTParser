
from urllib.parse import urlparse
import requests
from lib.controller.controller import task_push
from lib.core.common import isListLike, get_parent_paths
from lib.core.data import conf, KB, logger
from lib.core.enums import WEB_PLATFORM, OS, HTTPMETHOD
from lib.core.plugins import PluginBase
from lib.parse.parse_request import FakeReq
from lib.parse.parse_responnse import FakeResp

class W13SCAN(PluginBase):
    type = 'loader'
    desc = '''Loader插件对请求以及响应进行解析，从而调度更多插件运行'''
    name = 'plugin loader'
    def audit(self):
        headers = self.requests.headers
        url = self.requests.url
        p = urlparse(url)
        if not p.netloc:
            return
        for rule in conf.excludes:
            if rule in p.netloc:
                logger.info("Skip domain:{}".format(url))
                return
        
        exi = self.requests.suffix.lower()
        if exi == ".asp":
            self.response.programing.append(WEB_PLATFORM.ASP)
            self.response.os.append(OS.WINDOWS)
        elif exi == ".aspx":
            self.response.programing.append(WEB_PLATFORM.ASPX)
            self.response.os.append(OS.WINDOWS)
        elif exi == ".php":
            self.response.programing.append(WEB_PLATFORM.PHP)
        elif exi == ".jsp" or exi == ".do" or exi == ".action":
            self.response.programing.append(WEB_PLATFORM.JAVA)
        for name, values in KB["fingerprint"].items():
            if not getattr(self.response, name):
                _result = []
                for mod in values:
                    m = mod.fingerprint(self.response.headers, self.response.text)
                    if isinstance(m, str):
                        _result.append(m)
                    if isListLike(m):
                        _result += list(m)
                if _result:
                    setattr(self.response, name, _result)
        
        #if KB["spiderset"].add(url, 'PerFile'):
        task_push('PerFile', self.requests, self.response)
