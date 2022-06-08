
import copy
import threading
import time
import traceback
from lib.core.common import dataToStdout
from lib.core.data import KB, logger, conf

def exception_handled_function(thread_function, args=()):
    try:
        thread_function(*args)
    except KeyboardInterrupt:
        KB["continue"] = False
        raise
    except Exception:
        traceback.print_exc()

def run_threads(num_threads, thread_function, args: tuple = ()):
    threads = []
    try:
        info_msg = "Staring [#{0}] threads".format(num_threads)
        logger.info(info_msg)
        
        for num_threads in range(num_threads):
            thread = threading.Thread(target=exception_handled_function, name=str(num_threads),
                                      args=(thread_function, args))
            thread.setDaemon(True)
            try:
                thread.start()
            except Exception as ex:
                err_msg = "error occurred while starting new thread ('{0}')".format(str(ex))
                logger.critical(err_msg)
                break
            threads.append(thread)
        
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.is_alive():
                    alive = True
                    time.sleep(0.1)
    except KeyboardInterrupt as ex:
        KB['continue'] = False
        raise
    except Exception as ex:
        logger.error("thread {0}: {1}".format(threading.currentThread().getName(), str(ex)))
        traceback.print_exc()
    finally:
        dataToStdout('\n')

def start():
    run_threads(conf.threads, task_run)
def out_fuzz_prio_log():
    pass # KB["fuzz_req"].append([attackType,req_weight,position,self.requests,str(params)])
    KB["fuzz_req"] = sorted(KB["fuzz_req"], key=lambda req: req[1],reverse = True)
    f = open("./req_result/" + str(conf.id) + "_fuzzerlog.txt",'a')
    for i in KB["fuzz_req"]:
        f.write(i[0] + " - " + str(i[1]) + " - " + i[2] + " - " + i[3].netloc + " - " + i[4] + "\n")
def task_run():
    while KB["continue"] or not KB["task_queue"].empty():
        poc_module_name, request, response = KB["task_queue"].get()
        KB.lock.acquire()
        KB.running += 1
        if poc_module_name not in KB.running_plugins:
            KB.running_plugins[poc_module_name] = 0
        KB.running_plugins[poc_module_name] += 1
        KB.lock.release()
        printProgress()
        poc_module = copy.deepcopy(KB["registered"][poc_module_name])
        poc_module.execute(request, response) 
        KB.lock.acquire()
        KB.finished += 1
        KB.running -= 1
        if str(KB.running) == "0" and str(KB.task_queue.qsize()) == "0":
            out_fuzz_prio_log()
        KB.running_plugins[poc_module_name] -= 1
        if KB.running_plugins[poc_module_name] == 0:
            del KB.running_plugins[poc_module_name]
        KB.lock.release()
        printProgress()
    printProgress()
    
    

def printProgress():
    KB.lock.acquire()
    if conf.debug:
        
        KB.output.log(repr(KB.running_plugins))
    msg = '%d success | %d running | %d remaining | %s scanned in %.2f seconds' % (
        KB.output.count(), KB.running, KB.task_queue.qsize(), KB.finished, time.time() - KB.start_time)
    _ = '\r' + ' ' * (KB['console_width'][0] - len(msg)) + msg
    dataToStdout(_)
    KB.lock.release()

def task_push(plugin_type, request, response):
    for _ in KB["registered"].keys():
        module = KB["registered"][_]
        if module.type == plugin_type:
            KB["task_queue"].put((_, copy.deepcopy(request), copy.deepcopy(response)))
            # print('KB["task_queue"].put : ' , (_, copy.deepcopy(request), copy.deepcopy(response)))
            # KB["task_queue"].put :  ('command_system', <lib.parse.parse_request.FakeReq object at 0x7fc654cb9ef0>, <lib.parse.parse_responnse.FakeResp object at 0x7fc654cb95c0>)

def task_push_from_name(pluginName, req, resp):
    KB["task_queue"].put((pluginName, copy.deepcopy(req), copy.deepcopy(resp)))
