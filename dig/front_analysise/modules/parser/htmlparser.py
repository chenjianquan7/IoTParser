
from front_analysise.modules.parser.baseparse import BaseParser
from front_analysise.modules.parser.jsparser import JSParser
from front_analysise.tools.comm import JSFile
import os
import re

class HTMLParser(BaseParser):
    def __init__(self, filepath):
        self._js_codes = []
        self.jsfile_citations = {}
        BaseParser.__init__(self, filepath)
    def analysise(self):
        if os.path.isfile(self.fpath):
            content = ""
            self.log.debug("Start Analysise : {}".format(self.fpath))
            with open(self.fpath, "rb") as f:
                content = f.read()
            self.get_keyword(content)
            self.get_function(content)
            self.get_js_src(content)
            
            self._find_javascript_code(content)
            self.parse_jscode()
    def _find_javascript_code(self, html):
        """
        从HTML文件中寻找Javascript代码
        :param html: html代码
        :return: all 用户存放javascript代码片段的列表。
        """
        html_content = html.decode('utf-8', "ignore")
        js_codes = re.findall(r"<script>([\s\S]+?)</script>", html_content,re.I)
        js_codes = js_codes + re.findall(r"<script type=\"text/javascript\">([\s\S]+?)</script>", html_content,re.I)
        js_codes = js_codes + re.findall(r"<script language=\"JavaScript\">([\s\S]+?)</script>", html_content,re.I)
        # js_codes = js_codes + re.findall(r"<script type=\"text/javascript\">([\s\S]+?)</script>", html_content)
        b_js_codes = []
        for js_code in js_codes:
            res = js_code.encode("utf-8")
            b_js_codes.append(res)
        self._js_codes = b_js_codes
        
    def get_keyword(self, html):
        html_content = html.decode('utf-8', "ignore")
        
        name_list = re.findall(r'name="(.*?)"', html_content,re.I)
        id_list = re.findall(r'id="(.*?)"', html_content,re.I)
        
        php_request = re.findall(r"\$_REQUEST\['(.*?)'\]", html_content,re.I)
        php_get = re.findall(r"\$_GET\['(.*?)'\]", html_content,re.I)
        php_post = re.findall(r"\$_POST\['(.*?)'\]", html_content,re.I)
        php_cookie = re.findall(r"checkCookie\('(.*?)'\)", html_content,re.I) 
        
        asp_request = re.findall(r'Request_Form\("(.*?)"\)', html_content,re.I)
        print(asp_request)
        asp_tcwebApi_get = re.findall(r'TcWebApi_Set\(".*?",".*?","(.*?)"\)', html_content, re.I)
        print("asp_tcwebApi_get  ",asp_tcwebApi_get)
        

        results = set(name_list) | set(id_list) | set(php_request) | set(php_get) | set(php_post) | set(asp_request) | set(asp_tcwebApi_get) | set(php_cookie)
        for res in results:
            self._get_keyword(res, check=0)
    def get_function(self, html):
        html_content = html.decode('utf-8', "ignore")
        path_list = re.findall(r'action="(.*?)"', html_content)
        path_list2 = re.findall(r'"(/[a-zA-Z-_/]+\.asp)"',html_content,re.I)
        path_list3 = re.findall(r'"(/[a-zA-Z-_/]+\.php)"',html_content,re.I)
        path_list4 = re.findall(r'"(/[a-zA-Z-_/]+)"',html_content,re.I)
        
        results = set(path_list) | set(path_list2) | set(path_list3) | set(path_list4)
        for path in results:
            self._get_function(path, check=0)
    def get_js_src(self, html):
        html_content = html.decode('utf-8', 'ignore')
        src_list = re.findall(r'<script .*src="(.*?)"></script>', html_content,re.I)
        for src in src_list:
            res = src.find("?")
            if res > 0:
                src = src[:res]
            src_file = src.split("/")[-1]
            js_obj = self.jsfile_citations.get(src_file, JSFile(src))
            js_obj.add_depend(self.fpath)
            self.jsfile_citations.update({src_file: js_obj})

    def parse_jscode(self):
        for js in self._js_codes:
            tmp_keyword , tmp_functions = JSParser.parse_html_js(js)
            for key in tmp_keyword:
                self._get_keyword(key, check=0)
            for action in tmp_functions:
                self._get_function(action, check=0)
    def get_jsfile_citations(self):
        return self.jsfile_citations

if __name__ == "__main__":
    pass