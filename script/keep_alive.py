
import argparse
import os
import time
import requests
import sys

def main(ip,t):
    print("[+]start...")
    while True:
        try:
            res = requests.get("http://" + ip, timeout=5)
            print(".",end='')
        except:
            print("x",end='')
            os.popen("bash rollback.sh")
            time.sleep(0.5)
            os.popen("bash rollback.sh")
        sys.stdout.flush()
        time.sleep(int(t))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ip", dest="ip")
    parser.add_argument("-t", "--time", dest="time",nargs='?', default=2)
    args = parser.parse_args()
    # os.popen("bash snapshot.sh")
    # os.popen("bash snapshot.sh")
    main(args.ip,args.time)