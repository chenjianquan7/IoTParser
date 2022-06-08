
from front_analysise.untils.logger.logger import get_logger
from front_analysise.modules.analysise import FrontAnalysise, BackAnalysise
from front_analysise.untils.config import ANALYSIZER, B_FILTERS, F_FILTERS, API_SPLIT_MARCH, FROM_BIN_ADD, \
    UPNP_ANALYSISE
from front_analysise.untils.output import Output
from front_analysise.untils.tools import runtimer
from front_analysise.tools.upnpanalysise import UpnpAnalysise
from config import GHIDRA_SCRIPT, HEADLESS_GHIDRA
import datetime
import subprocess
import shutil
import argparse
import uuid
import os
import sys
sys.setrecursionlimit(5000) 
front_result_output = ""
ghidra_result_output = ""

log = get_logger()
scripts = {
    "ref2share": os.path.join(GHIDRA_SCRIPT, "ref2share.py"),
    "ref2sink_bof": os.path.join(GHIDRA_SCRIPT, "ref2sink_bof.py"),
    "ref2sink_cmdi": os.path.join(GHIDRA_SCRIPT, "ref2sink_cmdi.py"),
    "share2sink": os.path.join(GHIDRA_SCRIPT, "share2sink.py")
}

def argsparse():
    
    parser = argparse.ArgumentParser(description="SATC tool",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--directory", required=True, metavar="/root/path/_ac18.extracted",
                        help="Directory of the file system after firmware decompression")
    parser.add_argument("-id", "--id", required=True, metavar="1",
                        help="仿真生成的id")

    args = parser.parse_args()
    
    global front_result_output
    front_result_output = "./output"
    if not os.path.isdir(args.directory):
        log.error("Firmware path entered : {} not found".format(args.directory))
        sys.exit()
    
    if not os.path.isdir(front_result_output):
        log.info("Init output keyword_extract_result directory : {} ".format(front_result_output))
        os.makedirs(front_result_output)
    return args

def front_analysise(args):
    
    remove_keyword_collection = []
    remove_function_collection = []
    runtimer.set_step1()
    f_analysise = FrontAnalysise(args.directory)
    f_analysise.analysise(ANALYSIZER)
    runtimer.set_step2()
    f_res = f_analysise.get_analysise_result()
    f_remove_file = f_analysise.get_remove_file()
    
    upapanalysise = set()
    if UPNP_ANALYSISE:
        upnpanaly = UpnpAnalysise(args.directory)
        upapanalysise = upnpanaly.get_result()
    runtimer.set_step3()
    for _F in F_FILTERS:
        f = _F()
        f()
        remove_keyword = f.get_remove_keyword()
        remove_func = f.get_remove_functions()
        remove_keyword_collection = list(set(remove_keyword + remove_keyword_collection))
        remove_function_collection = list(set(remove_func + remove_function_collection))
    
    runtimer.set_step4()
    b_analysise = BackAnalysise(args.directory)
    b_analysise.analysise()
    names = b_analysise.getbinname_and_path()
    
    for _F in B_FILTERS:
        f = _F()
        f()
        remove_keyword = f.get_remove_keyword()
        remove_func = f.get_remove_functions()
        remove_keyword_collection = list(set(remove_keyword + remove_keyword_collection))
        remove_function_collection = list(set(remove_func + remove_function_collection))
        
        b_analysise.delete_function(remove_func)
        b_analysise.delete_keyword(remove_keyword)
    
    api_match_results = set()
    if API_SPLIT_MARCH:
        api_match_results = b_analysise.api_march()
    runtimer.set_end_time()
    
    res = b_analysise.get_result()

    
    o = Output(res, front_result_output, args.id)
    o.custom_write()
    o.write_file_info(f_res)

def main():
    start_time = datetime.datetime.now()
    log.info("Start analysis time : {}".format(str(start_time)))
    args = argsparse()
    bin_list = front_analysise(args)
    end_time = datetime.datetime.now()
    log.info("Total time : {}s".format((start_time-end_time).seconds))

if __name__ == "__main__":
    main()
