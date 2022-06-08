from front_analysise.modules.parser.baseparse import BaseParser
from front_analysise.untils.logger.logger import get_logger
import requests
import json
import os
import re

class JSParser(BaseParser):
    filepath = ""
    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)
        JSParser.filepath = filepath
    def parse_html_js(content):
        key_list = JSParser.get_keyword(content)
        results = JSParser.get_function(content)
        return key_list,results

    def analysise(self):
        if os.path.isfile(self.fpath):
            self.log.debug("Start Analysise : {}".format(self.fpath))
            with open(self.fpath, "rb") as f:
                content = f.read()
                key_list = self.get_keyword(content)
                for res in key_list:
                    self._get_keyword(res, check=0)
                results = self.get_function(content)
                for path in results:
                    self._get_function(path, check=0)
    @staticmethod
    def get_keyword(content):
        js_content = content.decode('utf-8', "ignore")
        
        key_list = re.findall(r'\s[a-zA-Z_0-9]+\.([a-zA-Z_0-9]+) = ', js_content,re.I)
        key_list2 = re.findall(r'\?([0-9a-zA-Z_\-\.]+)=', js_content,re.I)
        key_list3 = re.findall(r'&([0-9a-zA-Z_\-\.]+)=', js_content,re.I)
        
        results = set(key_list) | set(key_list2) | set(key_list3)
        return results
    @staticmethod
    def get_function(content):
        js_content = content.decode('utf-8', "ignore")
        
        get_path_list = re.findall(r'\$\.get\("(.*?)"', js_content,re.I)
        
        post_path_list = re.findall(r'\$\.post\("(.*?)"', js_content,re.I)
        
        ajax_path_list = re.findall(r'url\s?:\s?"(.*?)"', js_content,re.I)
        results = set(get_path_list) | set(post_path_list) | set(ajax_path_list)
        return results
        
    @staticmethod
    def _march_soapaction(code):
        code = code.decode('utf-8', "ignore")
        soapactions = re.findall(r'sendSOAPAction\("([\s\S]+?)",.*\)', code,re.I)
        return list(set(soapactions))