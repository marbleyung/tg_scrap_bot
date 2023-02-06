import asyncio
import datetime
import sys

from telethon import TelegramClient, types
from environs import Env
from telethon.tl.types import User

with open('log.txt', 'w', encoding='utf-8') as log:
    try:
        print('Hello')
        chat_type = int(input('0 - parse a CHANNEL\n1 - parse a CHAT'))
        if chat_type == 0:
            limit = int(input('How much messages you will parse?(1-50) '))
            if limit < 1 or limit > 50:
                raise ValueError('Limit of messages should be 1...50')
        else:
            limit = 1
        print('Connecting...')
        env = Env()
        env.read_env(r'.env')
        API_ID = env('API_ID')
        API_HASH = env('API_HASH')

        client = TelegramClient('anon', api_id=API_ID, api_hash=API_HASH)


        async def main(limit=1):
            me = await client.get_me()
            l = []
            print('Creating list of your channels... This might take a minute')
            async for i in client.iter_dialogs():
                entity = await client.get_entity(i)
                if isinstance(entity, User):
                    pass
                else:
                    l.append(entity)

            for i, j in enumerate(l):
                print(i, j.title)
            print('Here is the list of your channels')
            await asyncio.sleep(0.5)
            chat = int(input('Enter the number of the channel to parse: '))
            if chat < 0 or chat > len(l):
                raise IndexError(f'Channel number has to be in range 0...{len(l)}')

            now = datetime.datetime.now()
            time_format = "%H_%M_%S"
            chat = l[chat]
            messages = await client.get_messages(chat, limit=limit)
            messages_ids = [i.id for i in messages]
            print(messages_ids)
            with open(fr"{me.id}_{now:{time_format}}.html", 'w', encoding='utf-8') as file:
                userlist = []
                file.write('<table>\n')
                file.write('<tr>\n')
                file.write('<td>ID\n')
                file.write('<td>First Name</td>\n')
                file.write('<td>Last Name</td>\n')
                file.write('<td>Username</td>\n')
                file.write('<td>Phone</td>\n')
                file.write('</tr>\n')
                print('The process has been started. \n'
                      'Please dont close programm untill the end.\n'
                      'It might take some time (usually not more than few minutes)')
                if chat_type == 0:
                    for i in messages_ids:
                        try:
                            async for m in client.iter_messages(chat.id, reply_to=i, reverse=True):
                                if isinstance(m.sender, types.User):
                                    if m.sender.id not in userlist:
                                        userlist.append(m.sender.id)
                                        file.write('<tr>')
                                        file.write(f"<td>{str(m.sender.id)}</td>")
                                        userdata = [m.sender.first_name, m.sender.last_name,
                                                    m.sender.username, m.sender.phone]
                                        for data in userdata:
                                            if data is not None:
                                                file.write(f"<td>{data}</td>")
                                            else:
                                                file.write(f"<td>no data</td>")
                                        file.write('</tr>\n')
                        except Exception as e:
                            pass

                    file.write('</table>')
                    print('Successfully parsed')

                elif chat_type == 1:
                    async for i in client.iter_participants(chat):
                        if isinstance(i, types.User):
                            file.write('<tr>')
                            file.write(f"<td>{str(i.id)}</td>")
                            userdata = [i.first_name, i.last_name,
                                        i.username, i.phone]
                            for data in userdata:
                                if data is not None:
                                    file.write(f"<td>{data}</td>")
                                else:
                                    file.write(f"<td>no data</td>")
                            file.write('</tr>\n')
                    file.write('</table>')
                    print('Successfully parsed')

                else:
                    raise ValueError('Wrong channel type')
        with client:
            client.loop.run_until_complete(main(limit))

    except Exception as e:
        print(e)
        log.write(str(e))
