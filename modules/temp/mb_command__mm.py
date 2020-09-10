#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mb_command__mm.py
#
#  Copyright 2020 torsion <torsion@WALENTIN>

import sys
import minimalmodbus as mm
#import init_const as iconst


instrument = mm.Instrument(
						port='COM4',
                        slaveaddress=1,
                        close_port_after_each_call=True,
                        debug = True,
                        )
instrument.serial.baudrate = 115200
instrument.serial.timeout = 5
instrument.serial.mode = mm.MODE_RTU


ByteStringToSend = b"\x01\x2b\x0E\x01\x00\x70\x77"
Lbytestr = [1, 43, 14, 1, 0, 112, 119]


def read_one_reg(r=18):
    instrument.read_register(registeraddress=r,
                number_of_decimals=0,
                functioncode=3,
                signed=False)



if __name__ == '__main__':
    print(instrument)

##    wr = instrument.write_register(registeraddress=18,
##        value=13,
##        number_of_decimals=0,
##        functioncode=6,
##        signed=False,
##        )

##    rrr = instrument.read_long(
##                                registeraddress=33,
##                                functioncode=4,
##                                signed=False,
##                                byteorder=mm.BYTEORDER_BIG
##)

    rr = instrument.read_register(registeraddress=18,
                            number_of_decimals=0,
                            functioncode=3,
                            signed=False,)
    print(rr)

##    r = instrument.read_float(registeraddress=141, byteorder=0)
##    print(r)


