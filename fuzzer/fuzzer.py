from copy import deepcopy
import inspect
import os
import sys
from tabnanny import check
import threading
from tokenize import Token
import pickle
import json
import requests
from colorama import deinit
from queue import Queue
from lib.controller.controller import start, task_push_from_name
from lib.core.enums import HTTPMETHOD,PLACE, HTTPMETHOD
from lib.parse.parse_request import FakeReq
from lib.parse.parse_responnse import FakeResp
from lib.proxy.baseproxy import AsyncMitmProxy
from lib.parse.cmdparse import cmd_line_parser
from lib.core.data import logger, conf, KB
from lib.core.option import init

def version_check():
    if sys.version.split()[0] < "3.6":
        logger.error(
            "incompatible Python version detected ('{}'). To successfully run sqlmap you'll have to use version >= 3.6 (visit 'https://www.python.org/downloads/')".format(
                sys.version.split()[0]))
        sys.exit()

def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """
    try:
        _ = sys.executable if hasattr(sys, "frozen") else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)
    return os.path.dirname(os.path.realpath(_))

def main():
    version_check()
    
    root = modulePath()
    cmdline = cmd_line_parser()
    init(root, cmdline) 
    if conf.url or conf.url_file:
        urls = []
        if conf.url:
            urls.append(conf.url)
        if conf.url_file:
            urlfile = conf.url_file
            if not os.path.exists(urlfile):
                logger.error("File:{} don't exists".format(urlfile))
                sys.exit()
            with open(urlfile) as f:
                _urls = f.readlines()
            _urls = [i.strip() for i in _urls]
            urls.extend(_urls)
        for domain in urls:
            try:
                req = requests.get(domain)
            except Exception as e:
                logger.error("request {} faild,{}".format(domain, str(e)))
                continue
            fake_req = FakeReq(domain, {}, HTTPMETHOD.GET, "")
            fake_resp = FakeResp(req.status_code, req.content, req.headers)
            task_push_from_name('loader', fake_req, fake_resp)
        start()
    elif conf.server_addr:
        KB["continue"] = True 
        
        scanner = threading.Thread(target=start)
        
        
        
        api_pkl = os.path.exists('./req_result/' + str(conf.id) + '+api.pkl')
        no_api_pkl = os.path.exists('./req_result/' + str(conf.id) + '.pkl')
        if not(no_api_pkl): 
            print("[*]爬虫代理模式...")
            baseproxy = AsyncMitmProxy(server_addr=conf.server_addr, https=True)
            try:
                baseproxy.serve_forever()
            except KeyboardInterrupt:
                threading.Thread(target=baseproxy.shutdown, daemon=True).start()
                deinit() 
                print("\n[*] User quit")
            baseproxy.server_close()
        
        
            print("初始请求队列： ",len(KB["task_queue"].queue))

            
            queue_part1 = [] # queue会报错 TypeError: can't pickle _thread.lock objects
            for i in KB["task_queue"].queue:
                if "192.168" not in i[1]._url:
                    continue
                hhhhh = deepcopy(i)
                queue_part1.append(hhhhh)
            fn = './req_result/' + str(conf.id) + '.pkl' 
            with open(fn, 'wb+') as f:
                picklestring = pickle.dump(queue_part1, f) 
            
            f = open("./req_result/" + str(conf.id) + "_proxylog.txt",'w')
            f.write("");f.close()
            f = open("./req_result/" + str(conf.id) + "_proxylog.txt",'a')
            for i in range(KB["task_queue"].qsize()):
                req = KB["task_queue"].queue[i][1]
                f.write(req._method + " " + req._url + " " + str(req._post_data))
                f.write("\n")

        elif no_api_pkl and not(api_pkl): 
            print("[*]爬虫api模式...")
            baseproxy = AsyncMitmProxy(server_addr=conf.server_addr, https=True)
            try:
                baseproxy.serve_forever()
            except KeyboardInterrupt:
                threading.Thread(target=baseproxy.shutdown, daemon=True).start()
                deinit() 
                print("\n[*] User quit")
            baseproxy.server_close()
            
            fn = './req_result/' + str(conf.id) + '.pkl' 
            with open(fn, 'rb+') as f:  
                queue_part1 = pickle.load(f)
            for i in queue_part1:
                KB["task_queue"].put(i)
            print("[*]初始请求队列+api 长度 : ",KB["task_queue"].qsize())
            
            f = open("./req_result/" + str(conf.id) + "_proxylog+api.txt",'w')
            f.write("");f.close()
            f = open("./req_result/" + str(conf.id) + "_proxylog+api.txt",'a')
            for i in range(KB["task_queue"].qsize()):
                req = KB["task_queue"].queue[i][1]
                f.write(req._method + " " + req._url + " " + str(req._post_data))
                f.write("\n")
        
            queue_part1 = [] # queue会报错 TypeError: can't pickle _thread.lock objects
            for i in KB["task_queue"].queue:
                if "192.168" not in i[1]._url:
                    continue
                hhhhh = deepcopy(i)
                queue_part1.append(hhhhh)
            fn = './req_result/' + str(conf.id) + '+api.pkl' 
            with open(fn, 'wb+') as f:
                picklestring = pickle.dump(queue_part1, f) 

        else: 
            if str(conf.api) == "1":
                fn = './req_result/' + str(conf.id) + '+api.pkl' 
                with open(fn, 'rb+') as f:  
                    queue_part1 = pickle.load(f)
                for i in queue_part1:
                    KB["task_queue"].put(i)
                print("[*]初始请求队列+api 长度 : ",KB["task_queue"].qsize())
            else:
                fn = './req_result/' + str(conf.id) + '.pkl' 
                with open(fn, 'rb+') as f:  
                    queue_part1 = pickle.load(f)
                for i in queue_part1:
                    KB["task_queue"].put(i)
                print("[*]初始请求队列 长度 : ",KB["task_queue"].qsize())
                
        
        f = open("./req_result/" + str(conf.id) + "_fuzzerlog.txt",'w')
        f.write("")
        f.close()
        try:
            scanner.start()
        except KeyboardInterrupt:
            scanner.join(0.1)

if __name__ == '__main__':
    main()
