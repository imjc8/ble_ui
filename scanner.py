import asyncio
import json
from bleak import BleakScanner
import bleak

deviceList = []

async def main():
    devices = await BleakScanner.discover()
    #print("Scan Started")
    for d in devices:
        deviceList.append(f"{d.address} {d.name}" )
                #print(d)
    if(len(deviceList) == 0):
        pass
        #print("No Devices Found")

asyncio.run(main())
print(json.dumps(deviceList),end='')