import ncclient
from ncclient import manager
from ncclient.operations import TimeoutExpiredError
import xmltodict
import xml.dom.minidom
import socket
import json

def connect(node):
        try:
                m = ncclient.manager.connect(
                        host = node, 
                        port = '2222', 
                        username = 'joao', 
                        password = 'cisco12345!', 
                        hostkey_verify = False,
                        device_params={'name':'nexus'},
                        allow_agent=False,
                        look_for_keys=False
                        )
                return m
        except:
                print("Unable to connect " + node)

def getVersion(node):
        try:
                int_filter = '''
                        <show xmlns="http://www.cisco.com/nxos:1.0">
                                <version></version>
                        </show>
                        '''
                m = connect(node)
                netconf_output = m.get(('subtree', int_filter))
                xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
                version = xml_doc.getElementsByTagName("mod:nxos_ver_str")
        except:
                return "Unable to get this node version"
        return "Version " + version[0].firstChild.nodeValue

def changeHostname(node, newhostname):
        try:
                update_hostname = '''
                        <configure xmlns="http://www.cisco.com/nxos:1.0">
                                <__XML__MODE__exec_configure>
                                        <hostname><name>%s</name></hostname>
                                </__XML__MODE__exec_configure>
                        </configure>
                '''
                configuration = ''
                m = connect(node)

                configuration += '<config>'
                configuration += update_hostname % (newhostname)
                configuration += '</config>'
                m.edit_config(target='running', config=configuration)
        except:
                return "Unable to change this node hostname"
        return "Config pushed successfuly!"

def Main():
        host = "127.0.0.1"
        port = 5000
            
        mySocket = socket.socket()
        mySocket.bind((host, port))
                
        mySocket.listen(5)
        conn, addr = mySocket.accept()
        print ("Connection from: " + str(addr))
        while True:
                message = conn.recv(1024).decode()
                if not message: break
                if message == "show version":
                        message = getVersion(host)
                elif (message.split())[0] == "hostname":
                        message = changeHostname(host,(message.split())[1])
                else:
                        message = "Sorry, IDK this command"
                conn.send(message.encode())                                    
        conn.close()
             
if __name__ == '__main__':
        Main()
