# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import asyncio
import uuid
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message
import json
import time
from random import randint

async def main():
    # Inputs/Ouputs are only supported in the context of Azure IoT Edge and module client
    # The module client object acts as an Azure IoT Edge module and interacts with an Azure IoT Edge hub
    module_client = IoTHubModuleClient.create_from_edge_environment()

    # Connect the client.
    await module_client.connect()

    # Send a filled out Message object
    async def send_test_message(i):
        msg = Message(json.dumps({'velocity':i,'device':'Machine'}))
        print('msg is: ' + str(msg))
        await module_client.send_message_to_output(msg, "output")
        print("done sending message to TransformModule")

    try:
        while True:
            await asyncio.gather(send_test_message(randint(45,65)))
            time.sleep(20)
    except:
        # Finally, shut down the client
        await module_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()