import platform
import asyncio
import logging
import struct
import sys

from bleak import BleakClient

sendFlag = True

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
        # is_paired = await client.pair(protection_level=1)
        # print(f"Paired: {is_paired}")

        while True:
            for service in client.services:
                for characteristics in service.characteristics:
                    if characteristics.uuid == "ace26f61-0b66-48f8-a3e5-a565e8924ae5":
                        print("HELLO WORLD")
                        max_volt = 100
                        sendData = bytearray([max_volt])
                        await client.write_gatt_char(characteristics.uuid, sendData, True)
                        print(sendData)
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


