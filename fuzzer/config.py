

THREAD_NUM = 31  
EXCLUDES = ["google", "lastpass", '.gov.']  
RETRY = 2  
TIMEOUT = 30  
LEVEL = 3  

PROXY_CONFIG_BOOL = False
PROXY_CONFIG = {
    # "http": "127.0.0.1:8080",
    # "https": "127.0.0.1:8080"
}
ABLE = ['command_system']  
#ABLE = ['command_system','js_sensitive_content','buffer_overflow','unauth','xss']  
DISABLE = []  
XSS_LIMIT_CONTENT_TYPE = True  

DEBUG = False

USE_REVERSE = False  
REVERSE_HTTP_IP = "127.0.0.1"  
REVERSE_HTTP_PORT = 9999  
REVERSE_DNS = "dnslog.w13scan.hacking8.com"
REVERSE_RMI_IP = "127.0.0.1"  
REVERSE_RMI_PORT = 10002  
REVERSE_SLEEP = 5  
