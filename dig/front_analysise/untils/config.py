
from front_analysise.modules.parser import HTMLParser, JSParser, DlinkHNAPXMLParser
from front_analysise.modules.filter.b_filter import Keyword_max_in_bin
from front_analysise.modules.filter.f_filter import Para_repeattime_in_front
ANALYSIZER = {
    "html": HTMLParser,
    "asp": HTMLParser,
    "php": HTMLParser,
    # "xml": DlinkHNAPXMLParser,
    "xml": HTMLParser,
    "js": JSParser
}
B_FILTERS = [
    
]
F_FILTERS = [
    Para_repeattime_in_front
]

SPECIAL_MID_NAME = [".so", ".ko"]
# SPECIAL_MID_NAME = [".ko"]

SPECIAL_COMMAND = ['ls', "pwd", "cat", "vim", "whoami", "printf", "cp", "which", "top", "echo", "ps", "unzip", "fdisk", "sleep", "kill", "vi", "mkdir", "touch","ifconfig", "grep","df", "uname", "awk", "chmod", "find","ln", "netstat","mv", "ssh-keygen", "wget", "curl", "busybox"]

BIN_KEYWORDS_HITS = 10
BIN_FUNCTION_HITS = 0

REMOVE_FILE = ["device.xml", "defaultvalue.xml", "jquery.js", "bootstrap.min.js", "bootstrap.js"]
# SPECIAL_PATH = ["help"]
SPECIAL_PATH = []

API_SPLIT_MARCH = False

FROM_BIN_ADD = True

UPNP_ANALYSISE = False
