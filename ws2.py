import sys
from optparse import OptionParser

from twisted.python import log
from twisted.internet import reactor, ssl

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

from base64 import b64encode

import time
import os
import glob
import subprocess

class IoTServicesClientProtocol(WebSocketClientProtocol):
    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def get_time():
        return str(int(time.time()))

    def get_cpu_temp():
        pTemp = subprocess.Popen("vcgencmd measure_temp",stdout=subprocess.PIPE, shell=True)
        (cpuTemp,err) = pTemp.communicate()
        return str(cpuTemp[5:-3])

    def sendToHCP(self):
        msg = '{"mode":"async", "messageType":"ee71d66528cc09922871", "messages":[{"sensor":"roomTemp", "value":"'+self.read_temp()+'", "timestamp":'+self.get_time()+'}]}'
        self.sendMessage(msg.encode('utf8'))

    def onOpen(self):
        self.sendToHCP()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            print("Text message received: {}".format(payload.decode('utf8')))


if __name__ == '__main__':
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    log.startLogging(sys.stdout)

    parser = OptionParser()

# interaction for a specific Device instance - replace 1 with your specific Device ID
    parser.add_option("-u", "--url", dest="url", help="The WebSocket URL", default="wss://iotmmsd059251trial.hanatrial.ondemand.com/com.sap.iotservices.mms/v1/api/ws/data/e203e513-4ba4-4544-b7a3-6bed7faa52d6")
    (options, args) = parser.parse_args()

    # create a WS server factory with our protocol
    ##
    factory = WebSocketClientFactory(options.url, debug=False)
    headers={'Authorization': 'Bearer ' + '56e7d5215dbede9951faef46ecf73275'}
    # print(headers)
    factory = WebSocketClientFactory(options.url, headers=headers, debug=False)
    factory.protocol = IoTServicesClientProtocol

    # SSL client context: default
    ##
    if factory.isSecure:
        contextFactory = ssl.ClientContextFactory()
    else:
        contextFactory = None

    connectWS(factory, contextFactory)
    reactor.run()