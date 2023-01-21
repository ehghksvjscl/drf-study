import os
import asyncio
import django

from channels.layers import get_channel_layer

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

async def main():
    channel_layer = get_channel_layer()

    message_dict = {'content': 'Hello, World!'}

    await channel_layer.send('hello', message_dict)
    response_dict = await channel_layer.receive('hello')
    is_equal = message_dict == response_dict
    print("송수신 메시지 일치 여부: ", is_equal)

asyncio.run(main())