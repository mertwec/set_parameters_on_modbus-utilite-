#!/usr/bin/env python

import serial
import time,sys
from pprint import pprint
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import serial.tools.list_ports



ser = serial.Serial(
	port='COM4',
	baudrate = 115200,
	parity='N',
	stopbits=serial.STOPBITS_ONE,
	bytesize=8,
	timeout=5,
)

def serial_ports():
       """ Lists serial port names

           :raises EnvironmentError:
               On unsupported or unknown platforms
           :returns:
               A list of the serial ports available on the system
       """
       if sys.platform.startswith('win'):
           ports = ['COM%s' % (i + 1) for i in range(256)]
       elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
           # this excludes your current terminal "/dev/tty"
           ports = glob.glob('/dev/tty[A-Za-z]*')
       elif sys.platform.startswith('darwin'):
           ports = glob.glob('/dev/tty.*')
       else:
           raise EnvironmentError('Unsupported platform')

       result = []
       for port in ports:
           try:
               s = serial.Serial(port)
               s.close()
               result.append(port)
           except (OSError, serial.SerialException):
               pass
       return result



def writereader(mcode, ):
    try:
        print(ser.port)
        pprint(ser.getSettingsDict())

        ser.write(mcode) 		# запись байта
        print('////////')
        RecievedData=b''
        step = 0
        while RecievedData==b'':
            time.sleep(0.5)
            if step<3:
                print('.......',step)
                step+=1
                data_left = ser.in_waiting  		# проверка полученного байта
                print(data_left)

                RecievedData = ser.read(data_left)
                #RecievedData = ser.readline(data_left)
            else:
                break
        print(RecievedData)
        print(list(RecievedData), '\n--------------')
        L=[hex(i) for i in RecievedData]
        print(L)
    finally:
        ser.close()

if __name__ == '__main__':

    print(serial_ports())


    ystavk=b'\x01\x03\x00\x10\x00\x02\xC5\xCE'

    param01 = b'\x01\x04\x00\x01\x00\x01\x60\x0A' #01 04 00 01 00 01 60 0A
    param012 = b'\x01\x04\x00\x01\x00\x03\xE1\xCB'
    param02 = b'\x01\x04\x00\x30\x00\x01\x31\xC5'

    ByteStringToSend = b"\x01\x2b\x0E\x01\x00\x70\x77"  # b'1 43, 14, 1, 0, 112, 119'
    readpo_v = b'\x01\x04\x00\x21\x00\x02\x21\xC1'

    write18r=b'\x01\x06\x00\x12\x00\x19\xE8\x05'
    read18r=b'\x01\x03\x00\x12\x00\x01\x24\x0F'

    writereader(ByteStringToSend)





