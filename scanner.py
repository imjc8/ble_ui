import asyncio
from bleak import BleakScanner

deviceList = []

async def main():
    devices = await BleakScanner.discover()
    print("Scan Started")
    for d in devices:
        deviceList.append(d)
        print(d)
    if(len(deviceList) == 0):
        print("No Devices Found")

asyncio.run(main())