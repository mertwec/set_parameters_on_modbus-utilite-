#!/usr/bin/env python

import serial
import time
from pprint import pprint
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


client= ModbusClient(method = "rtu",
                    port="COM5",
                    stopbits = 1,
                    bytesize = 8,
                    parity = 'N',
                    baudrate = 115200,

                    #retry_on_empty=True,
                    #retries=5,
                    )

#client.socket = serial.Serial(rtscts=True, port='COM5')

def read_registers(startAddress, degree=0, count_=1, unit_=1):
    '''Reading from a holding register with the below content.'''

    res = client.read_holding_registers(address=startAddress, count=count_, unit=unit_)

    if not res.isError():
        value_reg = res.registers
        print(res)
        print(value_reg)
        for i in range(len(value_reg)):
            value_reg[i] = value_reg[i]-2**16 if value_reg[i] & 2**15 else value_reg[i] # отрицательность значения
            print(value_reg[i]/10**degree)
    else:
        print(res)


def write_one_register(wr_addr, wr_value:int, deegree=0 ):
    wr_value=int(wr_value*10**deegree)
    print(wr_value)

    rq = client.write_register(address=wr_addr, value=wr_value)

    #assert(not rq.isError())

    print(rq)

def wr(adr, v, d):
    print(client.is_socket_open())
    #client.socket.rtscts = True
    write_one_register(wr_addr=adr, wr_value=v, deegree=d)
    time.sleep(0.5)
    #client.socket.rtscts = False
    read_registers(startAddress=adr, degree=d, count_=1)

if __name__ == '__main__':

    try:
        #Connect to the serial modbus server
        connection = client.connect()
        print (connection)
        if connection:
            write_one_register(18,30)
            #wr(18, 30, 0)
        else:
            print('Cannot connect to the Modbus Server/Slave')

    finally:
        client.close()
