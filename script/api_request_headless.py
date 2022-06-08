
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import argparse
import json
import time
import os
import requests

def main(ip,id):
    id = int(id)
    urls = []
    apis = json.loads(open("../dig_result/" + str(id) + ".api_result",'r').read())
    print("api: ",len(apis))
    for api in apis:
        if id == 2:
            urls.append("http://" + ip + "/" + api.rstrip('\n'))
        elif id == 4:
            urls.append("http://" + ip + "/admin/" + api.rstrip('\n'))
        elif id == 9:
            flag = 1
            for fuck in ["/usr","/sbin","/sys","/var","/etc","/runtime","<","/tmp","/www"]:
                if fuck in api:
                    flag = 0
            if api[-4:] != ".php":
                flag = 0
            if flag == 0:
                continue
            urls.append("http://" + ip + "/" + api.rstrip('\n'))
        elif id == 8:
            urls.append("http://" + ip + "/" + api.rstrip('\n'))
        elif id == 19:
            urls.append("http://" + ip + "/" + api.rstrip('\n'))
        elif id == 21:
            urls.append("http://" + ip + "/" + api.rstrip('\n'))
    filepaths = json.loads(open("../dig_result/" + str(id) + ".filepath_result",'r').read())
    print("filepaths: ",len(filepaths))
    for filepath in filepaths:
        if id == 2:
            filepath = filepath[filepath.index("/www/")+5:]
        elif id == 4:
            try:
                filepath = 'admin/' + filepath[filepath.index("/cgi-bin/")+9:]
            except:
                print(filepath)
        elif id == 9:
            if "/www/" in filepath: 
                filepath = filepath[filepath.index("/www/")+5:]
            else:
                continue 
        elif id == 8:
            if "/www/" in filepath: 
                filepath = filepath[filepath.index("/www/")+5:]
            else:
                continue 
        elif id == 19:
            if "/www/" in filepath: 
                filepath = filepath[filepath.index("/www/")+5:]
            else:
                continue 
        elif id == 21:
            if "/www/" in filepath: 
                filepath = filepath[filepath.index("/www/")+5:]
            else:
                continue 
        urls.append("http://" + ip + "/" + filepath.rstrip('\n'))
    result = []
    for url in urls:
        url = url.replace("//","/").replace("http:/","http://")
        result.append(url)
    return list(set(result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ip", dest="ip")
    parser.add_argument("-id", "--id", dest="id")
    args = parser.parse_args()
    urls = main(args.ip,args.id)
    id = int(args.id)
    print(len(urls))
    k = 0
    for url in urls:
        try:
            res = requests.get(url,timeout=5)
            if str(res.status_code) in ["404"]:
                print(404)
                continue
        except:
            try:
                res = requests.get(url,timeout=5)
                if str(res.status_code) in ["404"]:
                    print(404)
                    continue
            except:
                print("timeout")
                pass
        try:
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--proxy-server=http://127.0.0.1:7778")
            caps = {
                'loggingPrefs': {
                    'performance': 'ALL',
                }
            }
            prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
            }
            chrome_options.add_experimental_option('w3c', False) 
            chrome_options.add_experimental_option('prefs', prefs) 
            driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options, executable_path='./chromedriver')
            driver.set_page_load_timeout(15)
            if id in [2,4]:
                tmp_url = "http://admin:admin@" + url[7:]
            elif id in [8,21]:
                tmp_url = url
            elif id in [19]:
                tmp_url = "http://admin:password@" + url[7:]
                
            print("[*]",tmp_url,k,len(urls))
            k += 1
            try:
                driver.get(tmp_url)
            except:
                driver.get(tmp_url)
            if id == 8:
                cookies={"name" : "PHPSESSID", "value" : "5ada2ca2275d2ce269277493403c3eab"}
                driver.add_cookie(cookie_dict=cookies)
            inputs = driver.find_elements_by_tag_name("input")
            print("开始填值...")
            for i in inputs:
                try:
                    fuck = i.get_attribute("value")
                    
                    if id == 8: 
                        if not fuck:
                            i.send_keys("aaaaaaaaaaaa")
                        
                        #     i.send_keys(fuck + "1")
                    else:
                        if not fuck:
                            i.send_keys("192.168.0.1")
                except Exception as e:
                    pass
            try:
                submits = driver.find_elements_by_xpath('//*[@value="Apply"]') + driver.find_elements_by_xpath('//*[@value="Save"]') + driver.find_elements_by_xpath('//*[@value="save"]')+ driver.find_elements_by_xpath('//*[@value="Submit"]')\
                        + driver.find_elements_by_xpath('//*[@value="OK"]')+ driver.find_elements_by_xpath('//*[@value="Submit"]')+ driver.find_elements_by_xpath('//*[@value="submit"]')+ driver.find_elements_by_xpath('//*[@value="GO"]')\
                        + driver.find_elements_by_xpath('//*[@value="go"]')+ driver.find_elements_by_xpath('//*[@value="send"]')+ driver.find_elements_by_xpath('//*[@value="next"]')+ driver.find_elements_by_xpath('//*[@value="NEXT"]')\
                        + driver.find_elements_by_id('applyButton')+ driver.find_elements_by_id('Add')

                print("开始提交...")
                if len(submits) == 0:
                    continue
                for submit in submits:
                    print(submit.get_attribute("value"))
                    submit.click()
            except Exception as e:
                print(e)
            time.sleep(3)
            try:
                driver.close()
            except: 
                pass
            os.popen("bash rollback.sh")
            os.popen("bash rollback.sh")
        except Exception as e:
            print(e)
            
            print(e.__traceback__.tb_frame.f_globals["__file__"])
            
            print(e.__traceback__.tb_lineno)

