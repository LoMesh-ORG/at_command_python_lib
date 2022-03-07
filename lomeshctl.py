import threading
from uci import Uci

from loMesh import LoMeshHandle

class LomeshCtl():
    def __init__(self):
        self.ssinkEpoch = None
        self.loMeshHandle = None
        self.readRate = None

        u = Uci()

        baud = u.get("lomesh", "lomeshconf", "baud")
        parity = u.get("lomesh", "lomeshconf", "parity")
        port = u.get("lomesh", "lomeshconf", "port")
        self.loMeshHandle = LoMeshHandle(baud, parity, port)
        self.isSink = True if '1' in u.get("lomesh", "lomeshconf", "sink") else False

        self.readRate = u.get("lomesh", "lomeshconf", "rate")

    def setSink(self):
        self.loMeshHandle.setSink()
    
    def readMessage(self):
        return self.loMeshHandle.lastMessage()

    def run(self):
        if self.isSink None == self.ssinkEpoch and time.time() - self.ssinkEpoch > 5 * 60:
            self.setSink()
            self.ssinkEpoch = time.time()
        
        print(self.readMessage())

        T = threading.Timer(self.readRate, self.run)
        T.setDaemon(True)
        T.start()
    
if __name__ == "__main__":
    loMeshObj = LomeshCtl()

    loMeshObj.run()
