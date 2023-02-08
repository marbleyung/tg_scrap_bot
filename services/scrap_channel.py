import asyncio

from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import User


async def create_groups_list(api_id, api_hash, username):
    client = TelegramClient(str(username), api_id=api_id, api_hash=api_hash)
    await client.connect()
    me = await client.get_me()
    l = []
    async for i in client.iter_dialogs():
        entity = await client.get_entity(i)
        if isinstance(entity, User):
            pass
        else:
            l.append(entity)
    user_groups = []
    for i, j in enumerate(l):
        user_groups.append([i, {j.title}])
    user_groups_2 = ''
    for i in user_groups:
        user_groups_2 += f'{i[0]} - {str(i[1])[2:-2]}\n'
    await client.disconnect()
    return user_groups_2, l


async def parse_my_groups(api_id, api_hash, username, chat_type, limit, chat_number):
    client = TelegramClient(username, api_id=api_id, api_hash=api_hash)
    await client.connect()
    me = await client.get_me()
    entities = []
    async for i in client.iter_dialogs():
        entity = await client.get_entity(i)
        if isinstance(entity, User):
            pass
        else:
            entities.append(entity)
    if chat_number < 0 or chat_number > len(entities):
        raise IndexError(f'Channel number has to be in range 0...{len(entities)}')

    chat = entities[chat_number]
    messages = await client.get_messages(chat, limit=limit)
    messages_ids = [i.id for i in messages]

    with open(fr"{me.id}.html", 'w', encoding='utf-8') as file:
        userlist = []
        file.write('<table>\n')
        file.write('<tr>\n')
        file.write('<td>ID\n')
        file.write('<td>First Name</td>\n')
        file.write('<td>Last Name</td>\n')
        file.write('<td>Username</td>\n')
        file.write('<td>Phone</td>\n')
        file.write('</tr>\n')
        if chat_type == 0:
            for i in messages_ids:
                try:
                    async for m in client.iter_messages(chat.id, reply_to=i, reverse=True):
                        if isinstance(m.sender, User):
                            if m.sender.id not in userlist:
                                if m.sender.username is not None:
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

        elif chat_type == 1:
            async for i in client.iter_participants(chat):
                if isinstance(i, User):
                    if i.username is not None:
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

        else:
            raise ValueError('Wrong channel type')
    await client.disconnect()


async def find_channel(keyword, api_id, api_hash, username):
    client = TelegramClient(session=username, api_id=api_id, api_hash=api_hash)
    await client.connect()
    result = await client(SearchRequest(q=keyword, limit=100))
    groups = [i for i in result.chats]
    with open(f'{username}.html', 'w', encoding='utf-8') as file:
        file.write('<table>\n')
        file.write('<tr>\n')
        file.write('<td>ID\n')
        file.write('<td>Title</td>\n')
        file.write('<td>Date created</td>\n')
        file.write('<td>Username</td>\n')
        file.write('<td>Participants count</td>\n')
        file.write('</tr>\n')
        try:
            group = []
            for i in groups:
                data = [i.id, i.title, i.date.strftime('%d.%m.%Y'), i.username, i.participants_count]
                group.append(data)
            group.sort(key=lambda x: x[-1], reverse=True)
            for i in group:
                file.write('<tr>')
                for j in i:
                    file.write(f"<td>{str(j)}</td>")
                file.write('</tr>\n')
            status = 'Succesfully parsed'
        except Exception as status:
            pass

        file.write('</table>')
    await client.disconnect()
    return status


async def parse_group_by_id(limit, chat, api_id, api_hash, username):
    client = TelegramClient(username, api_id=api_id, api_hash=api_hash)
    await client.connect()
    messages = await client.get_messages(chat, limit=limit)
    messages_ids = [i.id for i in messages]
    with open(fr"{username}.html", 'w', encoding='utf-8') as file:
        userlist = []
        file.write('<table>\n')
        file.write('<tr>\n')
        file.write('<td>ID\n')
        file.write('<td>First Name</td>\n')
        file.write('<td>Last Name</td>\n')
        file.write('<td>Username</td>\n')
        file.write('<td>Phone</td>\n')
        file.write('</tr>\n')
        for i in messages_ids:
            try:
                async for m in client.iter_messages(chat, reply_to=i, reverse=True):
                    if isinstance(m.sender, User):
                        if m.sender.id not in userlist:
                            if m.sender.username is not None:
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
                print('except block', e)

        file.write('</table>')
        print('Successfully parsed')
        await client.disconnect()


async def large_parse(limit, api_id, api_hash, username, keyword):
    client = TelegramClient(username, api_id=api_id, api_hash=api_hash)
    await client.connect()
    result = await client(SearchRequest(q=keyword, limit=100))
    groups = [i for i in result.chats]
    chats, channels = [], []
    for i in groups:
        if i.megagroup is True or i.gigagroup is True:
            chats.append(i)
        else:
            channels.append(i.username)
    print('Groups have been successfully parsed')
    print('Parsing users...')
    print(chats, channels)
    all_messages = []
    for channel in channels:
        messages = await client.get_messages(channel, limit=limit)
        messages_ids = [i.id for i in messages]
        all_messages.append(messages_ids)

    with open(fr"{username}.html", 'w', encoding='utf-8') as file:
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
        for c in channels:
            for i in all_messages:
                for j in i:
                    try:
                        async for m in client.iter_messages(c, reply_to=j, reverse=True):
                            if isinstance(m.sender, User):
                                if m.sender.id not in userlist:
                                    if m.sender.username is not None:
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

        for c in chats:
            try:
                async for i in client.iter_participants(c):
                    if isinstance(i, User) and i.username is not None:
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
            except Exception as e:
                print('Exception: ', e)
        file.write('</table>')
        print('Successfully parsed')
    await client.disconnect()
