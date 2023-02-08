LEXICON_EN = {'start': '🔍This bot can collect telegram users data just in few clicks\n'
                       '📖This process calls "parsing". To get familiar with it press "INFO"\n'
                       '🆕If you never used this bot, read info, then come back and start "SESSION"\n'
                       'Already registered? Press "parse"',
              'instructions': '1. Login on https://my.telegram.org\n'
                              '2. Press "API development tools" and create a new app. Use any name and link\n'
                              '3. Send your App api_id, App api_hash and phone number\n'
                              'example: 12345678 a123b4cd968ab57cf529e770a9f17d28 +380123456789',
              'info': '❗️PARSING is a process of collecting different data, such as telegram users usernames\n'
                      'It is completely legal\n'
                      '❗️GROUP, CHAT, CHANNEL - group is telegram entity with more than 2 users in it. '
                      'Chat and channel is different kinds of group:'
                      'CHAT is group, where all participants can communicate with each other,'
                      'while CHANNEL is a group, where only certain people can make posts\n'
                      'more info: https://appsgeyser.com/blog/telegram-channel-vs-telegram-group/\n'
                      '❗️LIMIT - the bigger number you enter, more users you will get,'
                      ' but the script will run longer too.'
                      'Now it can be up to 10, but in further it can be increased.\n'
                      '❓QUESTIONS OR SUGGESTIONS: raskolbrd@gmail.com',
              'help': 'COMMON PROBLEMS:\n'
                      'Error: The key is not registered in the system (caused by SearchRequest).\n'
                      'Fix: This is authentication error. Use /del and then create new session (/start).\n'
                      'You might also terminate current session in telegram.\n'
                      '❓YOUR PROBLEM IS NOT IN LIST: raskolbrd@gmail.com',
              'parsing_options': '1. PARSE MY GROUPS - bot creates list of your groups, you have to send the number of group to parse\n'
                                 '2. PARSE GROUP BY LINK/USERNAME - you have to send channel username or link to parse it\n'
                                 '3. FIND GROUPS - find groups by keyword\n'
                                 '4. LARGE PARSING - first it find groups by keyword and then parse each group automatically, instead of parse each group by link\n'
              }