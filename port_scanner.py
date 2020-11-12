import socket
import common_ports

port_dict = common_ports.ports_and_services

def get_open_ports(target, port_range, verb = False):
    open_ports = []
    port_string, hostByAddr, hostByName = ("", "", "")
    start, stop = port_range

    #checking validity of 'target' with first port in range
    try: socket.getaddrinfo(target, port_range[0])
    except:
      if target[0].isdigit() and target[1].isdigit(): return 'Error: Invalid IP address'
      else: return 'Error: Invalid hostname'

    #getting host name/address for verbose
    if target[0].isdigit() and target[1].isdigit() and verb:
      hostByAddr = target
      try: hostByName = socket.gethostbyaddr(target)[0]
      except: hostByName = None
    elif verb:
      hostByAddr = socket.gethostbyname(target)
      hostByName = target    

    def portCheck(host, port):
      testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      testSocket.settimeout(0.2)
      if testSocket.connect_ex((target, port)):
        #print('Port', port, 'closed.')
        testSocket.close()
        return False
      else:
        #print('Port', port, 'open.')
        testSocket.close()
        return True


    for port in range(start,stop+1):
      if portCheck(target, port):
        open_ports.append(port)

    if verb:
      if hostByName is not None: port_string = 'Open ports for ' + hostByName + ' (' + hostByAddr + ')\n'
      else: port_string = 'Open ports for ' + hostByAddr + "\n"
      port_string += 'PORT     SERVICE'
      for port in open_ports:
        #add spaces to end of port as string due
        #to format the supplied testing expects
        port = str(port)
        while len(port) < 4: port += " "
        port_string += "\n" + port + "     " + port_dict[int(port)]
      return port_string

    else: return open_ports
