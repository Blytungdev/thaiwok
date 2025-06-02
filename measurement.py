# /// script
# dependencies = [
#   "huawei-solar",
#   "pyserial",
#   "tzlocal",
# ]
# ///
from huawei_solar import AsyncHuaweiSolar, register_names as rn
import asyncio
import json
from datetime import datetime
from tzlocal import get_localzone

slave_id = 1

async def main(): 
    client = await AsyncHuaweiSolar.create_rtu("/dev/ttyUSB1", 9600, slave_id)
    results = await client.get_multiple([rn.PV_01_VOLTAGE, rn.PV_01_CURRENT], slave_id)

    timestamp = datetime.now(get_localzone()).isoformat()
    voltage = results[0].value
    current = results[1].value

    payload = {
        "timestamp": timestamp,
        "voltage": voltage,
        "current": current
    }
    print(json.dumps(payload))

asyncio.run(main())