import pylink
from cmsis_svd.parser import SVDParser
import cmsis_svd.data
import os
import functools
import json
import time

class JLink(pylink.JLink):
    # Store device rather than svd object, as parsing to device takes much time. So store this in ram.
    svd_device = None

    def __init__(self, device_name):
        pylink.JLink.__init__(self, lib=pylink.library.Library(dllpath=os.getcwd()+os.path.sep+'JLinkARM.dll'))
        if self.num_connected_emulators() == 0:
            print ('No emulator connected. Leaving...')
            exit()
        elif self.num_connected_emulators() == 1:
            self.open()
        else:
            print ('List of available emulators:')
            print(self.connected_emulators())
            print ('Enter serial number of emulator which shall be connected:')
            snum = input()
            self.open(snum)
        
        svd = SVDParser.for_mcu(device_name)
        if svd is None:
            print('SVD parser input parameters could not be determined')
            exit()
         
        self.svd_device = svd.get_device()
        
        self.connect(device_name, verbose=True)
        
        self.restart()
        
        self.rtt_start()

    @functools.lru_cache(maxsize=128)
    def get_reg_address(self, peripheral_name, register_name):
        addr = None
        if not self.svd_device is None:
            p = next((x for x in self.svd_device.peripherals if x.name == peripheral_name), None)
            if not p is None:
                r = next((x for x in p.registers if x.name == register_name), None)
                if not r is None:
                    addr = p.base_address + r.address_offset
        return addr

    def modify_register(self, peripheral_name, register_name, bitmask, value):
        reg_addr = self.get_reg_address(peripheral_name, register_name)
        if not reg_addr is None:
            self.memory_write32(reg_addr, [self.memory_read32(reg_addr, 1)[0] & (~ bitmask) | value])

    def read_register(self, peripheral_name, register_name):
        reg_addr = self.get_reg_address(peripheral_name, register_name)
        if not reg_addr is None:
            return self.memory_read32(reg_addr, 1)[0]

    def gpio_setmode(self, peripheral_name, pin_num, mode):
        self.modify_register(peripheral_name, 'MODER', (0b11 << pin_num*2), (mode << pin_num*2))

    def gpio_setoutput(self, peripheral_name, pin_num, output):
        self.modify_register(peripheral_name, 'ODR', (0b1 << pin_num), (output << pin_num))
    
    def gpio_getinput(self, peripheral_name, pin_num):
        return (self.read_register(peripheral_name, 'IDR') >> pin_num) & 1

    def rpc_exec(self, funcId, params):
        if self.halted():
            raise Exception('RPC will not respond in halted mode.')
        
        req_obj = {}
        req_obj['f']=funcId
        req_obj['p']=params
        bytes_written = self.rtt_write(0, bytes(str(req_obj)+str('\0'), 'ascii'))
        if bytes_written < len(str(req_obj)) + 1:
            raise Exception('Could not send full rpc request. Is RTT config BUFFER_SIZE_DOWN too small? Increase to 256.')
        response = []
        start_time = time.time()
        while not _is_json(''.join(chr(i) for i in response)):
            if time.time() - start_time > 10:
                raise Exception('Timeout waiting for rcp response.')
            response = response + self.rtt_read(0, 200)
        result = json.loads(''.join(chr(i) for i in response))
        if 'err' in result.keys():
            raise Exception('Target error \"' + result['err'] + '\" occured.')
        return json.loads(''.join(chr(i) for i in response))['p']

def _is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
