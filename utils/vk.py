import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import redis
import bot_common
 
r = redis.Redis(decode_responses=True)
vk_session = vk_api.VkApi(token='bab2fc4be18ce9a4436de292b5272ee98880fb1dd26ca2ac082b29b4846a8de5341bb0d5c6cbba162d3db', api_version=5.95)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 185018457)

commands = ['/reg', '/account', '/reset', '/help']
 
AAA = None
BBB = None
CCC = None
 
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.object.text.lower() == '/reg':
            mh = vk.messages.getHistory(peer_id=event.object.peer_id, count=200)
            for msgg in mh['items']:
                if "Вы успешно зарегистрировались" in msgg["text"]:
                    AAA = 'A'
            if AAA is None:
                uid, passwd = bot_common.new_account(r)
                r.set(f"passwd", "uid")
                vk.messages.send(peer_id=event.object.peer_id, message="[🎉] Вы успешно зарегистрировались\n\n[🔥] Ваш логин: " + str(uid) + "\n[🔥] Ваш пароль " + str(passwd), random_id=0)
            else:
               vk.messages.send(peer_id=event.object.peer_id, message='Вы уже зарегистрированы', random_id=0)
            AAA = None
        if event.object.text.lower() == '/account':
            msghistory1 = vk.messages.getHistory(peer_id=event.object.peer_id, count=200)
            for msg in msghistory1['items']:
                if "[🎉] Вы успешно зарегистрировались" in msg["text"]:
                    BBB = 'B'
                    CCC = msg["text"]
            if BBB is not None:
                vk.messages.send(peer_id=event.object.peer_id, message=CCC.replace("[🎉] Вы успешно зарегистрировались", ""), random_id=0)
            BBB = None
            CCC = None
        if event.object.text.lower() == '/help':
            vk.messages.send(peer_id=event.object.peer_id, message='× Команды бота:\n[📓] /reg - зарегистрировать аккаунт\n[🔑] /account - получить данные от аккаунта\n[⚒] /reset - сбросить аккаунт', random_id=0)
        if event.object.text.lower() not in commands:
            vk.messages.send(peer_id=event.object.peer_id, message='[❗] Такой команды не существует. Введите /help для просмотра всех команд', random_id=0)
        for count in range(len('/reset')):
            if event.object.text.lower().find('/reset') >= 0:
                passwd = (event.object.text.lower().replace('/reset ', ''))
                if not passwd:
                    vk.messages.send(peer_id=event.object.peer_id, message='Ваш аккаунт не создан', random_id=0)
                else:
                    uid = r.get(passwd)
                    bot_common.reset_account(r, uid)
                    vk.messages.send(peer_id=event.object.peer_id, message='[❗] Ваш аккаунт был сброшен', random_id=0)
            break  