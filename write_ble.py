from datetime import datetime
from decimal import DivisionByZero
import platform
import asyncio
import logging
import struct
import sys
import tkinter as tk
import csv
import argparse
import time

from bleak import BleakClient

sendFlag = True
sendOnce = True
running = True



fd = open('data_raw.csv','w')
writer_raw = csv.writer(fd)


fd2 = open('data.csv','w+')
writer = csv.writer(fd2)

DAC_OFFSET = 3.3/2
ADC_OFFSET = 0
GAIN = -100000

def count_to_float_adc(count, vref, bits, ext_offset):
    gain = 10*(2**bits)/(2*vref)    
    return (count*10/gain) - ext_offset
    #return (vref/(2**bits - 1) *count) - ext_offset
def count_to_float_dac(count, vref, bits, ext_offset):
    #gain = 10*(2**bits)/(2*vref)    
    #return (count*10/gain) - ext_offset
    return -((vref/(2**bits - 1) *count) - ext_offset)

def voltage_to_current(volt):
    return (30.303*volt - 50) * 1e-6



def notification_handler(sender, data):
    # print(', '.join('{:02x}'.format(x) for x in data))
    # print(int.from_bytes(data, "little"))
    #print(f"val hex {data.hex()} float {struct.unpack('f',data)} ")
    # print(sys.getsizeof(data))
    # print(data[0]);
    # print(int.from_bytes(data[0:1],"little"))

    # print(data)
    # print(f" {data.hex()}")11

    #dacVal = data[0:4]
    #adcVal = data[4:8]
    rx_dat = struct.iter_unpack('HH', data)
    for unpack_dat in rx_dat:
        print(f"dac count {unpack_dat[0]} adc count {unpack_dat[1]}")
        #print(dacVal)
        writer_raw.writerow(unpack_dat)
        dac_volt = count_to_float_dac(unpack_dat[0],3.3,12,DAC_OFFSET)
        adc_volt = count_to_float_adc(unpack_dat[1],3.3,12,ADC_OFFSET)
        print(f"dac volt {dac_volt} adc volt {adc_volt} current {voltage_to_current(adc_volt)}")
        writer.writerow((dac_volt,voltage_to_current(adc_volt)))



def notification_handler2(sender, data):
    # print(', '.join('{:02x}'.format(x) for x in data))
    # print(int.from_bytes(data, "little"))
    #print(f"val hex {data.hex()} float {struct.unpack('f',data)} ")
    # print(sys.getsizeof(data))
    # print(data[0]);
    # print(int.from_bytes(data[0:1],"little"))

    # print(data)
    # print(f" {data.hex()}")

    #dacVal = data[0:4]
    #adcVal = data[4:8]
    global running
    rx_dat = int.from_bytes(data,byteorder='little')
    print(f"Current state is {rx_dat}")
    if rx_dat == 5:
        running = False

    # works with 2 uints
    # dataPacket = bytearray(data);
    # DacHighByte = data[1]
    # DacLowByte = data[0]
    # DacHighByteConv = DacHighByte << 8
    # dacVal = DacHighByteConv | DacLowByte
    
    # AdcHighByte = data[3]
    # AdcHighByteConv = AdcHighByte << 8
    # AdcLowByte = data[2]
    # adcVal = AdcHighByteConv | AdcLowByte
    # printing works here
    # print(f"DAC: {dacVal}\t ADC: {adcVal}")

async def run(address, loop, min_volt=0,max_volt=3.3,start_volt=0,scan_rate=1,dir=False,numCycles=3, debug=False):
    global sendOnce
    log = logging.getLogger(__name__)
    if debug:
        loop.set_debug(True)
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))
        # is_paired = await client.pair(protection_level=1)
        # print(f"Paired: {is_paired}")

        while running:
            for service in client.services:
                for characteristics in service.characteristics:
                    # float send 3b7b5251-740d-4429-88f2-2e9b94fcb7aa
                    # int send ace26f61-0b66-48f8-a3e5-a565e8924ae5
                    if characteristics.uuid == "0852723d-4e9e-4c32-adc4-284dad4e4c30":

#                       value = bytes(await client.read_gatt_char(characteristics.uuid))
#                        print("value is: ", int.from_bytes(value, "little"))

                        #print(f"val hex {value.hex()} float {struct.unpack('f',value)} ")
                        # value=value.decode("UTF-8")
                        # print(type(value))
                        # print("value is: ", value)
                        # await asyncio.sleep(1)

                        await client.start_notify(characteristics.uuid, notification_handler)
                    if characteristics.uuid == "0852723d-4e9e-4c32-adc4-284dad4e4c31":

#                       value = bytes(await client.read_gatt_char(characteristics.uuid))
#                        print("value is: ", int.from_bytes(value, "little"))

                        #print(f"val hex {value.hex()} float {struct.unpack('f',value)} ")
                        # value=value.decode("UTF-8")
                        # print(type(value))
                        # print("value is: ", value)
                        # await asyncio.sleep(1)

                        await client.start_notify(characteristics.uuid, notification_handler2)

                    if characteristics.uuid == "3b7b5251-740d-4429-88f2-2e9b94fcb7aa" and sendOnce:
                        print("HELLO WORLD")
                        # parameters to send
                        #min_volt =0
                        #max_volt =3.3
                        #start_volt = 0 
                        #scan_rate = 0.5
                        #dir = True
                        #numCycles = 2

                        # convert to byte array
                        
                        minVoltData = bytearray(struct.pack("f", -max_volt + DAC_OFFSET))
                        maxVoltData = bytearray(struct.pack("f", -min_volt + DAC_OFFSET))
                        startVoltData = bytearray(struct.pack("f", start_volt + DAC_OFFSET))
                        scanRateData = bytearray(struct.pack("f", scan_rate))
                        dirData = bytearray([dir])
                        numCyclesData = bytearray([numCycles])
                        
                        # make byte string
                        sendData = minVoltData + maxVoltData + startVoltData + scanRateData + dirData + numCyclesData
                        await client.write_gatt_char(characteristics.uuid, sendData, True)
                        print(sendData)
                        print("DONE SENDINGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
                        sendOnce = False
        raise DivisionByZero


        # for service in client.services:
        #     log.info("[Service] {0}: {1}".format(service.uuid, service.description))
        #     for char in service.characteristics:
        #         if "read" in char.properties:
        #             try:
        #                 value = bytes(await client.read_gatt_char(char.uuid))
        #             except Exception as e:
        #                 value = str(e).encode()
        #         else:
        #             value = None
        #         log.info(
        #             "\t[Characteristic] {0}: ({1}) | Name: {2}, Value: {3} ".format(
        #                 char.uuid, ",".join(char.properties), char.description, value
        #             )
        #         )
        #         for descriptor in char.descriptors:
        #             value = await client.read_gatt_descriptor(descriptor.handle)
        #             #log.info("\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(descriptor.uuid, descriptor.handle, bytes(value)))
        #         if char.uuid == "d61b813c-1c78-4e8d-8e4e-548d29a87530":
        #             await client.write_gatt_char(char.uuid, b'\x01', False)
        #         #await client.write_gatt_char(char.uuid, b'Info=100', False)
        #         log.info('write completed')

if __name__ == "__main__":
    address = (
        #"00:a0:50:e8:8a:bd"
        "00:A0:50:D5:31:22"
        if platform.system() != "Darwin"
        else "6CFF7923-7B84-41D3-B021-C823949216C1"
    )
    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("min_volt", type=float)
    parser.add_argument("max_volt",type=float)
    parser.add_argument("start_volt",type=float)
    parser.add_argument("scan_rate",type=float)
    parser.add_argument("cycle",type=int)
    parser.add_argument("-d", "--down", help="increase output verbosity",
                    action="store_true")

    args = parser.parse_args()
    if args.down:
        direction = True
    else:
        direction = False
    now = datetime.now()
    try:
        loop.run_until_complete(run(address, loop, min_volt=args.min_volt, max_volt=args.max_volt, start_volt=args.start_volt, scan_rate=args.scan_rate, dir=direction, numCycles=args.cycle))
    except DivisionByZero:
        pass
    print("Finished experiment")
    fd2.close()
    if direction:
        direction_str = 'down'
    else:
        direction_str = 'up'
    with open(f"data_{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}.csv", 'a') as output_file, open(f"data.csv",'r') as input_file:
        output_file.write(f"# Params: min_volt {args.min_volt} max_volt {args.max_volt} start_volt {args.start_volt} scan_rate {args.scan_rate} direction {direction_str} num_cycles {args.cycle}\n")
        output_file.write("Stimulation voltage (V),Measured current(A)\n")
        output_file.write(input_file.read())
    
    #copy to a new file
