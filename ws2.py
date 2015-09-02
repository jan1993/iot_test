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

    def sendToHCP(self):
# send message of Message Type 1 and the corresponding payload layout that you defined in the IoT Services Cockpit
        self.sendMessage('{"mode":"async", "messageType":"ee71d66528cc09922871", "messages":[{"sensor":"sensor1", "value":"20", "timestamp":1413191650}]}'.encode('utf8'))

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