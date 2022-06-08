
import argparse
import json
import os
import time
import signal
 
 

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
    print(len(urls))
    for url in urls:
        print(url)
    