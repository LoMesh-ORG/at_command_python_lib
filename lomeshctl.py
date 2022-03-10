import json
import threading
import queue

import paho.mqtt.client as mqtt
from uci import Uci

from loMesh import LoMeshHandle

mqtt_iaq_topic_base  = '/device/sensor'
mqttReportTopicBase  = 'tbl/collect/'

clientLoc = None
loMeshObj = None

class LomeshCtl():
    def __init__(self):
        self.ssinkEpoch = None
        self.loMeshHandle = None
        self.readRate = None
        self.message_queue = queue.Queue()

        u = Uci()

        baud = u.get("lomesh", "lomeshconf", "baud")
        parity = u.get("lomesh", "lomeshconf", "parity")
        port = u.get("lomesh", "lomeshconf", "port")
        self.loMeshHandle = LoMeshHandle(baud, parity, port)
        self.isSink = True if '1' in u.get("lomesh", "lomeshconf", "sink") else False

        self.readRate = u.get("lomesh", "lomeshconf", "rate")

    def getMsgQueue(self):
        return self.message_queue

    def setSink(self):
        self.loMeshHandle.setSink()
    
    def readMessage(self):
        return self.loMeshHandle.lastMessage()  

    def runFragmentation(self):
        while True:
            msg = self.message_queue.get()
            jsonobj = json.loads(msg)

            msg1 = f"IAQ/{jsonobj["DID"]}/1/"
            msg2 = f"IAQ/{jsonobj["DID"]}/2/"

            if("sensor" in jsonobj):
                for element in jsonobj["sensor"]:
                    if "T" in element["2"]:
                        msg1 += f"T/{element["3"]}/"
                    elif "HUM" in element["2"]:
                        msg1 += f"HUM/{element["3"]}/"
                    elif "Co2" in element["2"]:
                        msg1 += f"Co2/{element["3"]}/"
                    elif "TVoc" in element["2"]:
                        msg1 += f"TVoc/{element["3"]}\n"

                    if "PM2.5" in element["2"]:
                        msg2 += f"PM2.5/{element["3"]}/"
                    elif "PM10" in element["2"]:
                        msg2 += f"PM10/{element["3"]}/"
                    elif "Co" in element["2"]:
                        msg2 += f"Co/{element["3"]}/"
                    elif "O3" in element["2"]:
                        msg2 += f"O3/{element["3"]}\n"
            print(msg1)
            print(msg2)

            T = threading.Timer(self.readRate, self.runFragmentation)
            T.setDaemon(True)
            T.start()

    def runAssembly(self):
        if self.isSink None == self.ssinkEpoch and time.time() - self.ssinkEpoch > 5 * 60:
            self.setSink()
            self.ssinkEpoch = time.time()
        
        print(self.readMessage())

        T = threading.Timer(self.readRate, self.runAssembly)
        T.setDaemon(True)
        T.start()

def iaqTopicControl(client, obj, msg):
    global loMeshObj

    loMeshObj.getMsgQueue().append(msg.payload.decode("utf-8"))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def localConnectionCbk(client, userdata, flags, rc):
    global clientLoc
    clientLoc.subscribe(mqtt_iaq_topic_base, 0)

def mqttConnect():
    global clientLoc
    clientLoc = mqtt.Client()
    #client.username_pw_set(username="nypd007",password="Nypd007!")
    #Subscript to all iaq topics
    clientLoc.message_callback_add(mqtt_iaq_topic_base, iaqTopicControl) 
    clientLoc.on_message = on_message
    clientLoc.on_connect = localConnectionCbk
    clientLoc.connect('127.0.0.1', 1883, 60)
    clientLoc.loop_forever()

if __name__ == "__main__":
    global loMeshObj

    loMeshObj = LomeshCtl()
    loMeshObj.runFragmentation()
    loMeshObj.runAssembly()

    mqttConnect()
