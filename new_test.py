import requests
import json
import requests
import time
from decouple import config

def auth_bet(uLogin: str, uPassword: str) -> list:
    cookies = {
        'lng': 'ru',
        '_ga_X2B11TMFNG': 'GS1.1.1655412395.40.1.1655412491.0',
        '_ga': 'GA1.1.1005467437.1655412395',
        'sh.session_be98639c': 'b01ed45d-1acf-4df7-b3d2-bffc18f7db84',
        'geocountry': 'ru',
        'tzo': '3',
        'SESSION': 'ea33ab8af26e5e4b199366a2d9a5bf37',
        'auid': 'F2nvfGKORnNfC2RTvTZbAg==',
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'melbet.ru',
        'Origin': 'https://melbet.ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://melbet.ru/user/registration/',
        # 'Content-Length': '62',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'lng=ru; _ga_X2B11TMFNG=GS1.1.1655412395.40.1.1655412491.0; _ga=GA1.1.1005467437.1655412395; sh.session_be98639c=b01ed45d-1acf-4df7-b3d2-bffc18f7db84; geocountry=ru; tzo=3; SESSION=ea33ab8af26e5e4b199366a2d9a5bf37; auid=F2nvfGKORnNfC2RTvTZbAg==',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'uLogin': uLogin,
        'uPassword': uPassword,
        'save': '',
    }

    response = requests.post('https://melbet.ru/user/auth/', cookies=cookies, headers=headers, data=data)
    with open("ErrorsFile.txt", "a") as file:
        file.write(f"\n++++++++++++++++++++++++++\n\n\nAUTH\n{response.text}\n")
    user_id = response.json()['userId']
    uhash = response.cookies["uhash"]
    return [user_id, uhash]

def check_cupones(user_id: int, uhash: str) -> list:
    cookies = {
            '_ga': 'GA1.1.1800826200.1655415999',
            '_ga_X2B11TMFNG': 'GS1.1.1655508012.41.1.1655508083.0',
            'lng': 'ru',
            'cfdata': '0c28e89d596d3c47973cf1c6a860827d%258e3b0499bafd52a3dbe895402285e414',
            'cur': 'RUB',
            'tzo': '3',
            'ua': f'{user_id}',
            'uhash': f"{uhash}",
            'geocountry': 'ru',
            'fixedFooter': '1',
            'unfixedRight': '1',
            'modeZoneSport3': '2',
            'login_tries': '0',
            'zsh': '1',
            'sh.session_be98639c': 'c9639afe-7134-489c-93a4-87a3453393de',
            'SESSION': 'ea33ab8af26e5e4b199366a2d9a5bf37',
            'auid': 'F2nvfGKORnNfC2RTvTZbAg==',
        }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ru',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'melbet.ru',
        'Origin': 'https://melbet.ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://melbet.ru/office/history/',
        # 'Content-Length': '105',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '_ga=GA1.1.1800826200.1655415999; _ga_X2B11TMFNG=GS1.1.1655508012.41.1.1655508083.0; lng=ru; cfdata=0c28e89d596d3c47973cf1c6a860827d%258e3b0499bafd52a3dbe895402285e414; cur=RUB; tzo=3; ua=413020545; uhash=3080cec956f1d84c9e5362d8528229bd; geocountry=ru; fixedFooter=1; unfixedRight=1; modeZoneSport3=2; login_tries=0; zsh=1; sh.session_be98639c=c9639afe-7134-489c-93a4-87a3453393de; SESSION=cb78ea4e61ee50f0e635b358560d6a50; auid=F2nvfGKORnNfC2RTvTZbAg==',
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.post('https://melbet.ru/user/balance/', cookies=cookies, headers=headers)
    print(response.json())

uLogin = config('LOGIN')
uPassword = config('PASSWORD')
auth = auth_bet(uLogin=uLogin, uPassword=uPassword)
user_id = auth[0]
uhash = auth[1]
checked_cupones = check_cupones(user_id=user_id, uhash=uhash)
