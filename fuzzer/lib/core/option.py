
import os
import threading
import time
from queue import Queue
from colorama import init as cinit
from cowpy.cow import milk_random_cow
from config import DEBUG, EXCLUDES, THREAD_NUM, LEVEL, \
    TIMEOUT, \
    RETRY, PROXY_CONFIG, PROXY_CONFIG_BOOL, DISABLE, ABLE, XSS_LIMIT_CONTENT_TYPE
from lib.core.common import random_UA, dataToStdout, ltrim, random_colorama
from lib.core.data import path, KB, logger, conf
from lib.core.exection import PluginCheckError
from lib.core.loader import load_file_to_module
from lib.core.output import OutPut
from lib.core.settings import VERSION, DEFAULT_USER_AGENT
from lib.core.spiderset import SpiderSet
from thirdpart.console import getTerminalSize
from thirdpart.requests import patch_all

class uniqueQueue(Queue): 
    def _put(self, item): # KB["task_queue"].put((_, copy.deepcopy(request), copy.deepcopy(response)))
        # print("====put=====",item,"===",item[1])
        flag = 1
        for i in self.queue:
            
            if i[0] == item[0] and i[1]._netloc == item[1]._netloc and str(i[1]._post_data.keys()) == str(item[1]._post_data.keys()) and str(i[1]._post_data.values()) == str(item[1]._post_data.values()) and str(i[1]._params.keys()) == str(item[1]._params.keys()):
                print("重复请求")
                flag = 0 
        if ".com/" in item[1]._url or str(item[2]._status_code) in ["400","500","404","403","502","503"] :
            print("错误请求")
            flag = 0
        if flag:
            self.queue.append(item)

def setPaths(root):
    path.root = root
    path.certs = os.path.join(root, 'certs')
    path.scanners = os.path.join(root, 'scanners')
    path.data = os.path.join(root, "data")
    path.fingprints = os.path.join(root, "fingprints")
    path.output = os.path.join(root, "output")

def initKb():
    KB['continue'] = False  
    KB['registered'] = dict()  
    KB['fingerprint'] = dict()  
    KB["task_queue"] = uniqueQueue()  
    KB["spiderset"] = SpiderSet()  
    KB["console_width"] = getTerminalSize()  
    KB['start_time'] = time.time()  
    KB["lock"] = threading.Lock()  
    KB["output"] = OutPut()
    KB["running_plugins"] = dict()
    KB["fuzz_req"] = []
    KB['finished'] = 0  
    KB["result"] = 0  
    KB["running"] = 0  

def initPlugins():
    
    for root, dirs, files in os.walk(path.scanners):
        files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
        for _ in files:
            q = os.path.splitext(_)[0]
            if conf.able and q not in conf.able and q != 'loader':
                continue
            if conf.disable and q in conf.disable:
                continue
            filename = os.path.join(root, _)
            mod = load_file_to_module(filename)
            try:
                mod = mod.W13SCAN()
                mod.checkImplemennted()
                plugin = os.path.splitext(_)[0]
                plugin_type = os.path.split(root)[1]
                relative_path = ltrim(filename, path.root)
                if getattr(mod, 'type', None) is None:
                    setattr(mod, 'type', plugin_type)
                if getattr(mod, 'path', None) is None:
                    setattr(mod, 'path', relative_path)
                KB["registered"][plugin] = mod
            except PluginCheckError as e:
                logger.error('Not "{}" attribute in the plugin:{}'.format(e, filename))
            except AttributeError:
                logger.error('Filename:{} not class "{}"'.format(filename, 'W13SCAN'))
    logger.info('Load scanner plugins:{}'.format(len(KB["registered"])))
    
    num = 0
    for root, dirs, files in os.walk(path.fingprints):
        files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
        for _ in files:
            filename = os.path.join(root, _)
            if not os.path.exists(filename):
                continue
            name = os.path.split(os.path.dirname(filename))[-1]
            mod = load_file_to_module(filename)
            if not getattr(mod, 'fingerprint'):
                logger.error("filename:{} load faild,not function 'fingerprint'".format(filename))
                continue
            if name not in KB["fingerprint"]:
                KB["fingerprint"][name] = []
            KB["fingerprint"][name].append(mod)
            num += 1
    logger.info('Load fingerprint plugins:{}'.format(num))

def _init_conf():
    conf.version = False
    conf.debug = DEBUG
    conf.level = LEVEL
    conf.server_addr = None
    conf.url = None
    conf.url_file = None
    conf.proxy = PROXY_CONFIG
    conf.proxy_config_bool = PROXY_CONFIG_BOOL
    conf.timeout = TIMEOUT
    conf.retry = RETRY
    conf.html = False
    conf.json = False
    conf.random_agent = False
    conf.agent = DEFAULT_USER_AGENT
    conf.threads = THREAD_NUM
    conf.disable = DISABLE
    conf.able = ABLE
    
    conf.excludes = EXCLUDES
    conf.XSS_LIMIT_CONTENT_TYPE = XSS_LIMIT_CONTENT_TYPE

def _merge_options(input_options):
    """
    Merge command line options with configuration file and default options.
    """
    if hasattr(input_options, "items"):
        input_options_items = input_options.items()
    else:
        input_options_items = input_options.__dict__.items()
    for key, value in input_options_items:
        
        if key not in conf:
            conf[key] = value
            continue
        if value:
            conf[key] = value

def _set_conf():
    
    if conf.version:
        exit()
    
    if isinstance(conf["server_addr"], str):
        defaulf = 7778
        if ":" in conf["server_addr"]:
            splits = conf["server_addr"].split(":", 2)
            conf["server_addr"] = tuple([splits[0], int(splits[1])])
        else:
            conf["server_addr"] = tuple([conf["server_addr"], defaulf])
    
    conf["threads"] = int(conf["threads"])
    
    if isinstance(conf["proxy"], str) and "@" in conf["proxy"]:
        conf["proxy_config_bool"] = True
        method, ip = conf["proxy"].split("@")
        conf["proxy"] = {
            method.lower(): ip
        }
    
    if conf.random_agent:
        conf.agent = random_UA()

def _init_stdout():
    
    if len(conf["excludes"]):
        logger.info("No scanning:{}".format(repr(conf["excludes"])))
    
    if conf.able:
        logger.info("Use plugins:{}".format(repr(conf.able)))
    
    if conf.disable:
        logger.info("Not use plugins:{}".format(repr(conf.disable)))
    logger.info("Level of contracting: [#{}]".format(conf.level))
    if conf.html:
        logger.info("Html will be saved in '{}'".format(KB.output.get_html_filename()))
    logger.info("Result will be saved in '{}'".format(KB.output.get_filename()))

def init(root, cmdline):
    cinit(autoreset=True) 
    setPaths(root) 
    banner()
    _init_conf()  
    _merge_options(cmdline)  
    _set_conf() 
    initKb() 
    initPlugins() 
    _init_stdout() 
    patch_all() 

def banner():
    msg = "w13scan v{}".format(VERSION)
    sfw = True
    s = milk_random_cow(msg, sfw=sfw)
    dataToStdout(random_colorama(s) + "\n\n")
