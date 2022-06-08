from front_analysise.modules.parameter import args_set, function_set
from front_analysise.modules.parameter.global_cls import Count
from front_analysise.untils.config import FROM_BIN_ADD
from front_analysise.untils.tools import runtimer, b_total
import os
import datetime
import json
import sys

class BaseOutput():
    def __init__(self, result, out_dir, firm_id):
        self.firm_id = firm_id
        self.baseoutdir = out_dir
        self.detailoutput = os.path.join(self.baseoutdir, "")
        self.simpleoutput = os.path.join(self.baseoutdir, "")
        if not os.path.isdir(self.detailoutput):
            os.makedirs(self.detailoutput)
        if not os.path.isdir(self.simpleoutput):
            os.makedirs(self.simpleoutput)
            os.makedirs(os.path.join(self.simpleoutput, ""))
        self.result = result
    def write_detail_function(self):
        pass
    def write_details_keyword(self):
        pass
    def write_back_result(self):
        pass
    def write_front_simple_keyword(self):
        pass
    def write_front_simple_function(self):
        pass
    def write_front_single_simple(self):
        pass

class Output(BaseOutput):
    def custom_write(self):
        self.write_detail_function()
        self.write_back_result()
    def write_detail_function(self):
        api_result_dict = []
        function_set.sort(key=lambda elem: elem.name)
        for function in function_set:
            api_result_dict.append(function.name)
        
        api_result_dict = json.dumps(api_result_dict, default=str)
        file = open(sys.path[0] + "/../dig_result/" + str(self.firm_id) + ".api_result", "w")
        file.write(api_result_dict)
        file.close()

    def write_back_result(self):
        bin_result_dict = {}
        self.keywords = set()
        self.function = set()
        self.other = set()
        self.other1 = set()
        for res in self.result:
            keywords = set()
            function = set()
            for r in res["keywords"]:
                string = r.get_match_str()
                for _r in string:
                    keywords.add(_r)
                if FROM_BIN_ADD:
                    string = r.get_bin_str()
                    for _r in string:
                        self.other.add(_r[0])
                        self.other1.add(_r)
                        keywords.add(_r[0])
            for r in res["functions"]:
                string = r.get_match_str()
                for _r in string:
                    function.add(_r)
            self.keywords = self.keywords | keywords
            self.function = self.function | function
            bin_result_dict[res["name"]] = keywords
        
        bin_result_dict = json.dumps(bin_result_dict, default=str)
        
        file = open(sys.path[0] + "/../dig_result/" + str(self.firm_id) + ".result", "w")
        file.write(bin_result_dict)
        file.close()
    def write_file_info(self, res):
        filepath_result = []
        for r in res:
            filepath_result.append(r.fpath)
            r.function_name.sort(key=lambda elem: elem.name)
            r.keyword_name.sort(key=lambda elem: elem.name)
        
        filepath_result = json.dumps(filepath_result, default=str)
        file = open(sys.path[0] + "/../dig_result/" + str(self.firm_id) + ".filepath_result", "w")
        file.write(filepath_result)
        file.close()
class JSONOutput(BaseOutput):
    def write_detail_function(self):
        pass
    def write_details_keyword(self):
        pass
    def write_back_result(self):
        pass
