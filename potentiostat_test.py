import platform
import asyncio
import logging
import struct
import sys

from bleak import BleakClient

sendFlag = True

# helper function
def notification_handler(sender, data):
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
    dacVal, adcVal = struct.unpack('HH', data)
    print(f"dac count {dacVal} adc count {adcVal}")
    #print(dacVal)


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



async def run(address, loop, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        loop.set_debug(True)
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))
        # paired = await client.pair(protection_level=1)
        # print(f"paired: {paired}")

        while True:
            for service in client.services:
                for characteristics in service.characteristics:
                    #0852723d-4e9e-4c32-adc4-284dad4e4c30
                    #a22c2cc0-faf3-498a-8607-55f4b322c1f3
                    if characteristics.uuid == "0852723d-4e9e-4c32-adc4-284dad4e4c30":

#                       value = bytes(await client.read_gatt_char(characteristics.uuid))
#                        print("value is: ", int.from_bytes(value, "little"))

                        #print(f"val hex {value.hex()} float {struct.unpack('f',value)} ")
                        # value=value.decode("UTF-8")
                        # print(type(value))
                        # print("value is: ", value)
                        # await asyncio.sleep(1)

                        await client.start_notify(characteristics.uuid, notification_handler)
                    global sendFlag
                    if (sendFlag):
                        print("HELLO WORLD")
                        write_UUID = "ace26f61-0b66-48f8-a3e5-a565e8924ae5"
                        # print(write_UUID)
                        # global sendFlag 
                        sendFlag = False
                        max_volt = 2
                        # sendData = bytearray([max_volt, min_volt, start_volt, direction_up, numCycles])
                        sendData = bytearray([max_volt])
                        print(sendData)
                        answer = await client.write_gatt_char(write_UUID, sendData, response=True)
                        print(answer)
                        print("DONE SENDINGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")



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
        "00:a0:50:e8:8a:bd"
        if platform.system() != "Darwin"
        else "6CFF7923-7B84-41D3-B021-C823949216C1"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))


