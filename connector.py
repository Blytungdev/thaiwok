from huawei_solar import AsyncHuaweiSolar, register_names as rn
import asyncio

inverter_modbus_id = 1

async def main(): 
    client = await AsyncHuaweiSolar.create_rtu("/dev/ttyUSB1", 9600, inverter_modbus_id)

    print("Connected")

    result = await client.get(rn.PV_01_VOLTAGE, inverter_modbus_id)

    print("PV_01_VOLTAGE: ", result.value)

asyncio.run(main())