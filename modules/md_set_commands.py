#-------------------------------------------------------------------------------
# Name:        md_set_commands
# Purpose:
#
# Author:      torsion
#
# Created:     31.08.2020
# Copyright:   (c) torsion 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import logging
import time
import sys
from pprint import pprint
import minimalmodbus as mm
import serial
import serial.tools.list_ports
import init_const

sys.path.append('..')
print(sys.version_info)
list_registers = (list(range(11,82+1))+
                list(range(107,115))+
                list(range(125,137))+
                list(range(139,162))+
                list(range(164,174)))

logging.basicConfig(filename="logfile.log",
                    format='%(asctime)s/ %(levelname)s:- %(message)s',
                    level=logging.INFO, filemode="w")

main_log = logging.getLogger("_log")

def init_instrument(port, baudrate=init_const.baudrate_):
    instrument = mm.Instrument(
    						port=port,
                            slaveaddress=1,
                            mode = mm.MODE_RTU,
                            close_port_after_each_call=True,
                            debug = False,
                            )
    instrument.serial.baudrate = baudrate
    instrument.serial.timeout = 5
    return instrument

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

def check_connect(instrument):
    # check connected (state of the system -- register 0)

    check = instrument.read_register(registeraddress=0,
                        functioncode=4)
    print('connected')
    main_log.info(f'Сonnection established, system check = {check}')
    return check


def select_port():
    try:
        ports = serial_ports()
        # ports = ['COM1','COM5','COM14']
        print(ports)
        if len(ports)==0:
            raise IndentationError
        else:
            for port in ports:
                try:
                    instrument=init_instrument(port)
                    if check_connect(instrument):
                        #instrument = init_instrument(port)
                        main_log.info(f'Connect to port: {port}')
                        return instrument
                    else:
                        main_log.info(f'Failed connect to port: {port}')
                except:
                    main_log.info(f'Failed connect to port: {port}')
                    continue

    except IndentationError or AttributeError:
        print('Can`t find connected device')
        main_log.error('Can`t find connected device')
    except IOError:
        print('Failed to read from instrument')
        main_log.error('Failed to read from instrument')


def read_one_register(register_, degree=0, signed_=False):
    try:
        r_one = instrument.read_register(registeraddress=register_,
                                number_of_decimals=degree,
                                functioncode=3,
                                signed=signed_)
        return r_one
    except Exception as e:
        print(e)
        main_log.error(f'Error reading: {e}')

def read_n_registers(start_register, numb_reg):
    registers_ = range(start_register, start_register+numb_reg+1)
    r_Nr = instrument.read_registers(registeraddress=start_register,
                                number_of_registers=numb_reg,
                                functioncode=3,)

    dict_value = dict(zip(registers_,r_Nr))
    return dict_value


def write_one_register(register_, value_, degree=0, signed_= False):
    try:
        instrument.write_register(registeraddress=register_,
                                    value=value_,
                                    number_of_decimals=degree,
                                    functioncode=6,
                                    signed=signed_,)
        print('writed')
    except Exception as e:
        print(e)
        main_log.error(f'Error writing: {e}')

def write_n_registers(start_register, values_:list): # functioncode = 16
    try:
        instrument.write_registers(registeraddress=start_register,
                                    values=values_
                                    )
        print('writed ')
    except Exception as e:
        print(e)


def read_all_registers(list_registers:list or range):
    list_value = []
    for i in list_registers:
        if i in range(141,162):
            list_value.append(read_one_register(i, degree=degree_, signed_=True))
        else:
            list_value.append(read_one_register(i, degree=degree_, signed_=False))
    return dict(zip(list_registers,list_value))

def read_settings_registers(settings_dict:dict):
    '''reading registers specified in init_config.py
    '''
    list_value = []
    list_registers=settings_dict.keys()
    for regist in list_registers:
        if regist in range(141,162):
            list_value.append(read_one_register(regist, degree=settings_dict.get(regist)[1], signed_=True))
        else:
            list_value.append(read_one_register(regist, degree=settings_dict.get(regist)[1], signed_=False))
    new_values_reg =dict(zip(list_registers,list_value))
    for _ in new_values_reg.keys():
        main_log.info(f'reading {_}: {new_values_reg[_]}')
    return new_values_reg


def write_settings(settings_dict:dict):
    '''writing registers specified in init_config.py
    '''
    for regist in settings_dict.keys():
        print(f'writing {regist} -- {settings_dict[regist][0]} in {settings_dict[regist][1]} ')
        main_log.info(f'writing {regist} -- {settings_dict[regist][0]} in {settings_dict[regist][1]} ')


        if regist in range(141,162):
            write_one_register (regist,
                                settings_dict.get(regist)[0],
                                degree=settings_dict.get(regist)[1],
                                signed_= True)

        else:
            write_one_register (regist,
                                settings_dict.get(regist)[0],
                                degree=settings_dict.get(regist)[1],
                                signed_= False)


if __name__ == '__main__':
    instrument = select_port()
    try:
        print(init_const.baudrate_)
        print(instrument)
        main_log.info(instrument.serial)

        write_settings(init_const.settings)
        main_log.info('-------------------------')
        pprint(read_settings_registers(init_const.settings ))


    except IOError as e:
        main_log.error(f'Error connect: {e}')
    except Exception as e:
        print(e)
        main_log.error(f'Total error: {e}')
    finally:
        instrument.serial.close()
        main_log.info('port close')
        input('press "Enter" for exit')
