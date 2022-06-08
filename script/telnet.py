import telnetlib

def run_telnet(host, command):
    tn = telnetlib.Telnet(host, port=31338, timeout=3)
    tn.set_debuglevel(0)
    tn.read_until(b'/ #')
    tn.write(command.encode('utf-8') + b'\n')
    try:
        hhh = tn.read_until(b'#')
    except:
        pass
    tn.close()
    hhh = hhh.split(b"\r\n")
    
    return hhh

result = run_telnet("192.168.1.1",'cat /tmp/os_cmd_injection_log')
result = " ".join('{}'.format(h) for h in result)
