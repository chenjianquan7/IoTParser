
import copy
import platform
import socket
import sys
import traceback
from urllib.parse import quote
import requests
from sympy import EX
import urllib3
from requests import ConnectTimeout, HTTPError, TooManyRedirects, ConnectionError
from urllib3.exceptions import NewConnectionError, PoolError
from lib.core.settings import VERSION
from lib.core.common import dataToStdout, createGithubIssue, url_dict2str
from lib.core.data import conf, KB
from lib.core.exection import PluginCheckError
from lib.core.output import ResultObject
from lib.parse.parse_request import FakeReq
from lib.parse.parse_responnse import FakeResp
from lib.core.common import splitUrlPath, updateJsonObjectFromStr
from lib.core.enums import POST_HINT, PLACE, HTTPMETHOD
from lib.core.settings import DEFAULT_GET_POST_DELIMITER, DEFAULT_COOKIE_DELIMITER

class PluginBase(object):
    def __init__(self):
        self.type = None
        self.path = None
        self.target = None
        self.requests: FakeReq = None
        self.response: FakeResp = None
        self.weight_keys = {}
    def new_result(self) -> ResultObject:
        return ResultObject(self)
    def success(self, msg: ResultObject):
        if isinstance(msg, ResultObject):
            msg = msg.output()
        elif isinstance(msg, dict):
            pass
        else:
            raise PluginCheckError('self.success() not ResultObject')
        KB.output.success(msg)
    def checkImplemennted(self):
        name = getattr(self, 'name')
        if not name:
            raise PluginCheckError('name')
    def audit(self):
        raise NotImplementedError
    def generateItemdatas(self, params=None):
        iterdatas = []
        if self.requests.method == HTTPMETHOD.GET:
            _params = params or self.requests.params
            iterdatas.append((_params, PLACE.GET))
        elif self.requests.method == HTTPMETHOD.POST:
            _params = params or self.requests.post_data
            iterdatas.append((_params, PLACE.POST))
        if conf.level >= 3:
            _params = self.requests.cookies
            iterdatas.append((_params, PLACE.COOKIE))
        
        
        
        return iterdatas
    def paramsCombination(self, data: dict, place=PLACE.GET, payloads=[], hint=POST_HINT.NORMAL, urlsafe='/\\'):
        """
        组合dict参数,将相关类型参数组合成requests认识的,防止request将参数进行url转义
        :param data:
        :param hint:
        :return: payloads -> list
        """
        result = []
        if place == PLACE.POST:
            if hint == POST_HINT.NORMAL:
                for key, value in data.items():
                    new_data = copy.deepcopy(data)
                    for payload in payloads:
                        new_data[key] = payload
                        result.append((key, value, payload, new_data))
            elif hint == POST_HINT.JSON:
                for payload in payloads:
                    for new_data in updateJsonObjectFromStr(data, payload):
                        result.append(('', '', payload, new_data))
        elif place == PLACE.GET:
            for payload in payloads:
                for key in data.keys():
                    temp = ""
                    for k, v in data.items():
                        if k == key:
                            temp += "{}={}{} ".format(k, quote(payload, safe=urlsafe), DEFAULT_GET_POST_DELIMITER)
                        else:
                            temp += "{}={}{} ".format(k, quote(v, safe=urlsafe), DEFAULT_GET_POST_DELIMITER)
                    temp = temp.rstrip(DEFAULT_GET_POST_DELIMITER)
                    result.append((key, data[key], payload, temp))
        elif place == PLACE.COOKIE:
            for payload in payloads:
                for key in data.keys():
                    temp = ""
                    for k, v in data.items():
                        if k == key:
                            temp += "{}={}{}".format(k, quote(payload, safe=urlsafe), DEFAULT_COOKIE_DELIMITER)
                        else:
                            temp += "{}={}{}".format(k, quote(v, safe=urlsafe), DEFAULT_COOKIE_DELIMITER)
                    result.append((key, data[key], payload, temp))
        elif place == PLACE.URI:
            uris = splitUrlPath(data, flag="<--flag-->")
            for payload in payloads:
                for uri in uris:
                    uri = uri.replace("<--flag-->", payload)
                    result.append(("", "", payload, uri))
        return result
    def req(self, position, params, attackType,req_weight, headers=None): 
        KB["fuzz_req"].append([attackType,req_weight,position,self.requests,str(params)])
        f = open("./req_result/" + str(conf.id) + "_fuzzerlog.txt",'a')
        f.write(attackType + " - " + str(req_weight) + " - " + position + " - " + self.requests.netloc + " - " + str(params) + "\n")
        print(attackType,position,self.requests.netloc, params)
        r = False
        if headers is None:
            headers = self.requests.headers
        if position == PLACE.GET:
            r = requests.get(self.requests.netloc, params=params, headers=headers, allow_redirects=False)
        elif position == PLACE.POST:
            r = requests.post(self.requests.url, data=params, headers=headers, allow_redirects=False)
        elif position == PLACE.COOKIE:
            headers = self.requests.headers
            if 'Cookie' in headers:
                del headers["Cookie"]
            if 'cookie' in headers:
                del headers["cookie"]
            if isinstance(params, dict):
                headers["Cookie"] = url_dict2str(params, PLACE.COOKIE)
            else:
                headers["Cookie"] = params
            if self.requests.method == HTTPMETHOD.GET:
                r = requests.get(self.requests.url, headers=headers, allow_redirects=False)
            elif self.requests.method == HTTPMETHOD.POST:
                r = requests.post(self.requests.url, data=self.requests.post_data, headers=headers,
                                  cookies=params, allow_redirects=False)
        elif position == PLACE.URI:
            r = requests.get(params, headers=self.requests.headers, allow_redirects=False)
        return r
    def execute(self, request: FakeReq, response: FakeResp):
        self.target = ''
        self.requests = request
        self.response = response
        output = None
        
        output = self.audit() 
        
        
        
        #     msg = 'Plugin: {0} not defined "{1} mode'.format(self.name, 'audit')
        #     dataToStdout('\r' + msg + '\n\r')
        
        
        
        #         msg = 'Plugin: {0} timeout, start it over.'.format(self.name)
        
        #             dataToStdout('\r' + msg + '\n\r')
        
        
        
        
        
        
        
        
        
        
        #         msg = "connect target '{0}' failed!".format(self.target)
        #         # Share.dataToStdout('\r' + msg + '\n\r')
        
        #     msg = 'Plugin: {0} HTTPError occurs, start it over.'.format(self.name)
        #     # Share.dataToStdout('\r' + msg + '\n\r')
        
        #     msg = "connect target '{0}' failed!".format(self.target)
        #     # Share.dataToStdout('\r' + msg + '\n\r')
        
        #     print("error...")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #     errMsg = "W13scan plugin traceback:\n"
        #     errMsg += "Running version: {}\n".format(VERSION)
        #     errMsg += "Python version: {}\n".format(sys.version.split()[0])
        #     errMsg += "Operating system: {}\n".format(platform.platform())
        
        #         errMsg += '\n\nrequest raw:\n'
        
        
        #     dataToStdout('\r' + errMsg + '\n\r')
        #     dataToStdout('\r' + excMsg + '\n\r')
        
        #         dataToStdout('\r' + "[x] a issue has reported" + '\n\r')
        return output
