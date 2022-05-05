import re
import serial
import sys


class LoMeshHandle:
    def __init__(self, baud, parity, port):
        self.baud = baud
        self.parity = parity
        self.port = port

    def getBaud(self):
        return self.baud

    def getParity(self):
        return self.parity

    def getPort(self):
        return self.port

    def setBaud(self, baud):
        self.baud = baud

    def setParity(self, parity):
        self.parity = parity

    def setPort(self, port):
        self.port = port

    def sendMessage(self, value, dest):
        try:
            with serial.Serial(
                self.port, self.baud, parity=self.parity, timeout=1
            ) as ser:
                if len(value) < 64:
                    ser.write(
                        b"AT+SEND:"
                        + str(dest).encode("utf-8")
                        + b"="
                        + str(value).encode("utf-8")
                        + b"\r\n"
                    )

        except Exception as e:
            print("Error in sending broadcast " + str(e))
        sys.stdout.flush()

    def lastMessage(self):
        result = ""
        try:
            # Create a serial object
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.reset_input_buffer()
                ser.write(b"AT+RECV?\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" not in data:
                    result = re.search("%s(.*)%s" % (":", "\r"), data).group(1)

        except Exception as e:
            print("Error in getting last message " + str(e))
        sys.stdout.flush()
        return result

    def softReset(self):
        try:
            with serial.Serial(
                self.port, self.baud, parity=self.parity, timeout=1
            ) as ser:
                ser.write(b"AT+RST\r\n")

        except Exception as e:
            print("Error in resetting the device " + str(e))
        sys.stdout.flush()

    def broadcastMessage(self, value):
        try:
            with serial.Serial(
                self.port, self.baud, parity=self.parity, timeout=1
            ) as ser:
                if len(value) < 64:
                    ser.write(b"AT+BCAST=" + str(value).encode("utf-8") + b"\r\n")

        except Exception as e:
            print("Error in sending broadcast " + str(e))
        sys.stdout.flush()

    def setSink(self):
        try:
            with serial.Serial(
                self.port, self.baud, parity=self.parity, timeout=1
            ) as ser:
                ser.write(b"AT+SETSINK\r\n")
        except Exception as e:
            print("Error in setting device as sink " + str(e))
        sys.stdout.flush()

    def sendSinkMessage(self, value):
        try:
            with serial.Serial(
                self.port, self.baud, parity=self.parity, timeout=1
            ) as ser:
                if len(value) < 64:
                    ser.write(b"AT+SSINK=" + str(value).encode("utf-8") + b"\r\n")

        except Exception as e:
            print("Error in sending message to sink " + str(e))
        sys.stdout.flush()

    def get_rx_queue(self):
        count = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.reset_input_buffer()
                ser.write(b"AT+RXCT?\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" not in data:
                    data.replace("\r", "")
                    data.replace("\n", "")
                    count = data

        except Exception as e:
            print("Error in getting last message " + str(e))
        sys.stdout.flush()

        return count

    def queryStatus(self):
        status = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=1
            ) as ser:
                ser.reset_input_buffer()
                ser.write(b"AT+MSGACK?\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    status = "NOT OK"
                else:
                    data.replace("\r", "")
                    data.replace("\n", "")
                    status = data

        except Exception as e:
            print("Error in getting last message " + str(e))
        sys.stdout.flush()
        return status

    def setCurrentAddress(self, address):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+ADDR=" + str(address).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting current address " + str(e))
        sys.stdout.flush()
        return result

    def getCurrentAddress(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+ADDR?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting current address " + str(e))
        sys.stdout.flush()
        return result

    def setNetworkAddress(self, address):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+NADDR=" + str(address).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting network address " + str(e))
        sys.stdout.flush()
        return result

    def getNetworkAddress(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+NADDR?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting network address " + str(e))
        sys.stdout.flush()
        return result

    def setEncryptionKey(self, encoded_key, key_type="A"):
        try:
            with serial.Serial(
                self.port, self.baud, parity=self.parity, timeout=1
            ) as ser:
                if len(encoded_key) < 32:
                    ser.write(
                        b"AT+AESKEY:"
                        + str(key_type).encode("utf-8")
                        + b"="
                        + str(encoded_key).encode("utf-8")
                        + b"\r\n"
                    )
                else:
                    raise ValueError("Encoded key length greater than 32 bytes")

        except Exception as e:
            print("Error in setting encryption key " + str(e))
        sys.stdout.flush()

    def getMACAddress(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+MAC?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting MAC address " + str(e))
        sys.stdout.flush()
        return result

    # TODO: verify this!
    def getModuleInformation(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+I?\r\n")
                data1 = ser.readline().decode("utf-8")
                data2 = ser.readline().decode("utf-8")
                data3 = ser.readline().decode("utf-8")
                data4 = ser.readline().decode("utf-8")
                result += data1.strip() + '\r\n'
                result += data2.strip() + '\r\n'
                result += data3.strip() + '\r\n'
                result += data4.strip() + '\r\n'

        except Exception as e:
            print("Error in getting module information " + str(e))
        sys.stdout.flush()
        return result

    def enterBootloader(self):
        status = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=1
            ) as ser:
                ser.reset_input_buffer()
                ser.write(b"AT+BOOTLOAD\r\n")
                data = ser.read_until().decode("utf-8")
                status = data.strip()

        except Exception as e:
            print("Error in entering bootloader " + str(e))
        sys.stdout.flush()
        return status

    def getActivityCounter(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+CADCOUNTER?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting activity counter " + str(e))
        sys.stdout.flush()
        return result

    def resetActivityCounter(self):
        status = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=1
            ) as ser:
                ser.reset_input_buffer()
                ser.write(b"AT+CADCOUNTERRST\r\n")
                data = ser.read_until().decode("utf-8")
                status = data.strip()

        except Exception as e:
            print("Error in resetting activity counter " + str(e))
        sys.stdout.flush()
        return status

    def getOpMode(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+MODE?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting operation mode " + str(e))
        sys.stdout.flush()
        return result

    def getRFChannel(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+RFCH?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting rf channel " + str(e))
        sys.stdout.flush()
        return result

    def setRFChannel(self, channel_no):
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+RFCH=" + str(channel_no).encode("utf-8") + b"\r\n")
        except Exception as e:
            print("Error in setting rf channel " + str(e))
        sys.stdout.flush()
        return

    def getTXPowerLevel(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+TXPOWER?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting TX power level " + str(e))
        sys.stdout.flush()
        return result

    def setTXPowerLevel(self, power_level):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+TXPOWER=" + str(power_level).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting TX power level " + str(e))
        sys.stdout.flush()
        return result

    def getCADRSSILevel(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+CADRSSI?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting CAD RSSI level " + str(e))
        sys.stdout.flush()
        return result

    def setCADRSSILevel(self, cadrssi_level):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+CADRSSI=" + str(cadrssi_level).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting CAD RSSI level " + str(e))
        sys.stdout.flush()
        return result

    def getSpreadingFactor(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+SF?\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = "NOT OK"
                else:
                    result = data.strip().split(":")[0].split('=')[1]

        except Exception as e:
            print("Error in getting spreading factor " + str(e))
        sys.stdout.flush()
        return result

    def setSpreadingFactor(self, spreading_factor):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+SF=" + str(spreading_factor).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting spreading factor " + str(e))
        sys.stdout.flush()
        return result

    def getUnreadMessageCount(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+RXCT?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting unread message count " + str(e))
        sys.stdout.flush()
        return result

    def getHopsTable(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+SHOWHOPS?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data  # it is a table

        except Exception as e:
            print("Error in getting hops table " + str(e))
        sys.stdout.flush()
        return result

    def setBaudRate(self, baud_rate):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+BAUD=" + str(baud_rate).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting baud rate " + str(e))
        sys.stdout.flush()
        return result

    def setUARTParity(self, parity_value):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+PARITY=" + str(parity_value).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting UART parity " + str(e))
        sys.stdout.flush()
        return result

    def setRSSIThreshold(self, threshold_value):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(
                    b"AT+GOODRSSI=" + str(threshold_value).encode("utf-8") + b"\r\n"
                )
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in setting RSSI threshold " + str(e))
        sys.stdout.flush()
        return result

    def getRSSIThreshold(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+GOODRSSI?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data.strip().split("=")[1]

        except Exception as e:
            print("Error in getting RSSI threshold " + str(e))
        sys.stdout.flush()
        return result

    def pingDevice(self, address):
        status = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=1
            ) as ser:
                ser.reset_input_buffer()
                ser.write(b"AT+PING:" + str(address).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    status = "NOT OK"
                else:
                    status = data.strip()

        except Exception as e:
            print("Error in getting last message " + str(e))
        sys.stdout.flush()
        return status

    def listALLMCASTIDS(self):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+MCASTID?\r\n")
                data = ser.read_until().decode("utf-8")
                result = data  # it is a newline padded list

        except Exception as e:
            print("Error in getting all MCAST IDs " + str(e))
        sys.stdout.flush()
        return result

    def addMCASTID(self, device_id):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+MCASTADD=" + str(device_id).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in adding MCAST ID " + str(e))
        sys.stdout.flush()
        return result

    def removeMCASTID(self, device_id):
        result = ""
        try:
            with serial.Serial(
                self.port, baudrate=self.baud, parity=self.parity, timeout=0.25
            ) as ser:
                ser.write(b"AT+MCASTREM=" + str(device_id).encode("utf-8") + b"\r\n")
                data = ser.read_until().decode("utf-8")
                if "NOT OK" in data:
                    result = data.strip().split(":")[1]

        except Exception as e:
            print("Error in removing MCAST ID " + str(e))
        sys.stdout.flush()
        return result
