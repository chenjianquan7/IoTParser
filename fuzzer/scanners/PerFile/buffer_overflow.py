
import copy
import random
import re
from urllib.parse import quote
import json
from matplotlib.font_manager import json_load
from lib.api.dnslog import DnsLogApi
from lib.api.reverse_api import reverseApi
from lib.core.common import generateResponse, random_str, updateJsonObjectFromStr, splitUrlPath, run_telnet, alive
from lib.core.data import conf
from lib.core.enums import OS, PLACE, VulType, POST_HINT
from lib.core.plugins import PluginBase
from lib.core.settings import acceptedExt, DEFAULT_GET_POST_DELIMITER, DEFAULT_COOKIE_DELIMITER

class W13SCAN(PluginBase):
    name = '溢出漏洞'
    desc = '''测试溢出漏洞'''
    def paramsCombination(self, data: dict, place=PLACE.GET, hint=POST_HINT.NORMAL, urlsafe='/\\'):
        """
        组合dict参数,将相关类型参数组合成requests认识的,防止request将参数进行url转义
        :param data:
        :param hint:
        :return: payloads -> list
        """
        result = []
        payloads = [i.rstrip('\n') for i in open("./dicts/bo.txt",'r').readlines()]
        
        if place == PLACE.POST:
            if hint == POST_HINT.NORMAL:
                for key, value in data.items():
                    for payload in payloads:
                        new_data = copy.deepcopy(data)  
                        new_data[key] = data[key] + payload  
                        
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
                            temp += "{}={}{}".format(k, quote(v + payload, safe=urlsafe),
                                                        DEFAULT_GET_POST_DELIMITER)
                        else:
                            temp += "{}={}{}".format(k, quote(v, safe=urlsafe), DEFAULT_GET_POST_DELIMITER)
                    temp = temp.rstrip(DEFAULT_GET_POST_DELIMITER)
                    result.append((key, data[key], payload, temp))
        elif place == PLACE.COOKIE:
            for payload in payloads:
                for key in data.keys():
                    temp = ""
                    for k, v in data.items():
                        if k == key:
                            temp += "{}={}{}".format(k, quote(v + payload, safe=urlsafe),
                                                        DEFAULT_COOKIE_DELIMITER)
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

    def calc_weight(self, key): 
        weight = 0
        dig_results = json.loads(open("../dig_result/" + str(conf.id) + ".result", 'r').read())
        for kk in dig_results.keys():
            if "'"+key+"'" in dig_results[kk]:
                weight += 1
                
        if weight > 3:
            weight = 0-weight*(0.1)
        self.weight_keys[key] = weight
        return weight

    def get_boflag(self, id): 
    
        logs = open("../../../FirmAE/scratch/" + str(conf.id) + "/qemu.final.serial.log").read()
        return logs.count('$ 0')

    def audit(self):
        url = self.requests.url
        if self.requests.suffix not in acceptedExt and conf.level < 4:
            return
        iterdatas = self.generateItemdatas()
        all_payloads = {}
        kkk = 0
        for origin_dict, positon in iterdatas:
            payloads = self.paramsCombination(origin_dict, positon)
            for payload in payloads :
                all_payloads[positon + str(kkk)] = [self.calc_weight(payload[0]),payload[0],payload[3]] 
                kkk += 1
        req_weight = 0
 
        for key in all_payloads.keys():
            tmp = key
            for i in range(10):
                tmp = tmp.replace(str(i),'')
            positon = tmp
            if conf.prio == "1":
               
                req_weight = self.weight_keys[all_payloads[key][1]] 
            flag_count1 = self.get_boflag(conf.id)
            r = self.req(positon, all_payloads[key][2],"BO",req_weight)
            html1 = r.text 
            flag_count2 = self.get_boflag(conf.id)
            print("flag_count1 : flag_count2 => ",flag_count1,flag_count2)
            if flag_count1 != flag_count2:
                print("flag_count1 : flag_count2 => ",flag_count1,flag_count2)
                print(" or router dead")
                result = self.new_result()
                result.init_info(url, "溢出", VulType.CMD_INNJECTION)
                result.add_detail("payload请求", r.reqinfo, generateResponse(r),
                                    "执行payload ", key, all_payloads[key][1], positon)
                self.success(result)
                break
