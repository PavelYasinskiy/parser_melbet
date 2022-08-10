import requests
import json
import datetime
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
    past = (datetime.datetime.today()-datetime.timedelta(days=3)).strftime("%d-%m-%Y")
    this_day = datetime.datetime.today().strftime("%d-%m-%Y")
    data = {
        'bonus': f'{user_id}',
        'from': f'{past}',
        'to': f'{this_day}',
        'fLine': '0',
        'fLive': '1',
        'fEst': '1',
        'fNot': '0',
        'fType': '-1',
        'fSort': '1',
        'buyInKassa': '0',
    }

    response = requests.post('https://melbet.ru/office/history', cookies=cookies, headers=headers, data=data)
    cupones_res = list()
    if "error" not in response.json().keys():
        message = response.json()["message"]
        num = 1
        while num > 0:
            num = 0
            num = message.find('class="number">Купон')
            if " " in message[num+22:num+22+11]:
                break
            cupone = message[num+22:num+22+11]
            message = message[num+22+11:]
            num = message.find('style="background: #')
            result = message[num+20:num+20+6]
            if result == "55C014":
                result = 0      #Победа
            elif result == "f97070":
                result = 1      #Проигрыш
            message = message[num+20+16:]
            cupones_res.append((cupone, result))
        return(cupones_res)

def balance_update(user_id: int, uhash: str, cupones_res:list) -> None:
    with open("balance.json", "r") as balance_file:
        balance_now = json.load((balance_file))
    with open("coupones.json", "r") as coupones_file:
        coupones_now = json.load((coupones_file))

    for _, coupone in enumerate(cupones_res):
        if (str(coupone[0]) in coupones_now.keys()) and (coupone[1] == 1):
            if coupones_now[str(coupone[0])]["match_result"] == 0:
                coupones_now[str(coupone[0])]["match_result"] = 2
                coupones_now[str(coupone[0])]["bet_true"] = 1
            elif coupones_now[str(coupone[0])]["match_result"] > 3:
                coupones_now.pop(str(coupone[0]))
            else:
                coupones_now[str(coupone[0])]["bet_true"] = 1
        elif (str(coupone[0]) in coupones_now.keys()) and (coupone[1] == 0):
            coupones_now.pop(str(coupone[0]))
    balance_from_site = balance_checker(user_id=user_id, uhash=uhash)

    if balance_now['balance']*2 <= balance_from_site:
        balance_now['balance'] = balance_from_site

    with open("balance.json", "w") as balance_file:
        json.dump(balance_now, balance_file, sort_keys=True, indent=20, ensure_ascii=False)
    with open("coupones.json", "w") as coupones_file:
        json.dump(coupones_now, coupones_file, sort_keys=True, indent=20, ensure_ascii=False)

def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num

def summ_bet_for_stadart() -> int:
    with open("balance.json", "r") as balance_file:
        balance = json.load((balance_file))
    balance_now = balance["balance"]
    summ_bet = round(600)
    if summ_bet < 15:
        summ_bet = 10
        return summ_bet
    elif 1000 > summ_bet >= 15:
        summ_bet = int_r(summ_bet / 10)
        return summ_bet*10
    elif 10000 > summ_bet >= 1000:
        summ_bet = int_r(summ_bet / 100)
        return summ_bet*100
    elif summ_bet >= 10000:
        summ_bet = int_r(summ_bet / 1000)
        return summ_bet*1000

def standart_bet(user_id: int, uhash:str, game_id: int, param: float, summ: int):
    cookies = {
        'lng': 'ru',
        '_ga_X2B11TMFNG': 'GS1.1.1655415999.40.1.1655416143.0',
        '_ga': 'GA1.1.1800826200.1655415999',
        'cfdata': 'b99ea673f776af3a164b1fc382c8144a%2500c5eb647939e2bdc75a676d261a7929',
        'cur': 'RUB',
        'login_tries': '0',
        'tzo': '3',
        'ua': f'{user_id}',
        'uhash': 'asd',
        'zsh': '1',
        'sh.session_be98639c': 'c9639afe-7134-489c-93a4-87a3453393de',
        'SESSION': 'ea33ab8af26e5e4b199366a2d9a5bf37',
        'geocountry': 'ru',
        'auid': 'F2nvfGKORnNfC2RTvTZbAg==',
    }

    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'If-Modified-Since': 'Sat, 1 Jan 2000 00:00:00 GMT',
        'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
        'Accept-Language': 'ru',
        'Cache-Control': 'no-cache',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'melbet.ru',
        'Origin': 'https://melbet.ru',
        # 'Content-Length': '278',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Referer': 'https://melbet.ru/live/basketball/2288083-belarus-sky-league/380935199-piranhas-astronauts/',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'lng=ru; _ga_X2B11TMFNG=GS1.1.1655415999.40.1.1655416143.0; _ga=GA1.1.1800826200.1655415999; cfdata=b99ea673f776af3a164b1fc382c8144a%2500c5eb647939e2bdc75a676d261a7929; cur=RUB; login_tries=0; tzo=3; ua=413020545; uhash=3080cec956f1d84c9e5362d8528229bd; zsh=1; sh.session_be98639c=c9639afe-7134-489c-93a4-87a3453393de; SESSION=cb78ea4e61ee50f0e635b358560d6a50; geocountry=ru; auid=F2nvfGKORnNfC2RTvTZbAg==',
        'X-Requested-With': 'XMLHttpRequest',
    }
    for i in range(33):
        json_data = {
            'UserId': f'{user_id}',
            'Events': [
                {
                    'GameId': game_id,
                    'Type': 9,
                    'Coef': 1.9,
                    'Param': param,
                    'PlayerId': 0,
                    'Kind': 1,
                    'Expired': 0,
                    'Price': 0,
                    'InstrumentId': 0,
                    'Seconds': 0,
                },
            ],
            'partner': 8,
            'Summ': summ,
            'Lng': 'ru',
            'Vid': 0,
            'hash': f'{uhash}',
            'Source': 5,
            'CheckCf': 2,
            'Live': True,
        }

        response = requests.post('https://melbet.ru/dataLineLive/put_bets_common.php', cookies=cookies, headers=headers,
                                 json=json_data)
        with open("ErrorsFile.txt", "a") as file:
            file.write(f"\nSTANDART BET{response.text}\n")
        cupone = response.json()
        if cupone["ErrorCode"] == 0:
            balance = cupone["Value"]["Balance"]
            coeffic = cupone["Value"]["Coupon"]["Coef"]
            parameter = cupone["Value"]["Coupon"]["Events"][0]['Param']
            bet_sum = cupone["Value"]["Coupon"]["Summ"]
            id_coup = cupone["Value"]["Id"]
            full_balance = balance+bet_sum
            coup = {f"{id_coup}": {"balance": balance,
                                   "full_balance": full_balance,
                                   "coef": coeffic,
                                   "parameter": parameter,
                                   "match_result": 0,
                                   "bet_sum": bet_sum,
                                   "bet_true": 0
                                   }}
            with open("coupones.json", "r") as coupones_file:
                new_coup = json.load(coupones_file)
                new_coup.update(coup)
            with open("coupones.json", "w") as coupones_file:
                json.dump(new_coup, coupones_file, sort_keys=True, indent=20, ensure_ascii=False)

            break
        elif cupone["ErrorCode"] in [131, 135]:
            time.sleep(1.5)
            continue
        elif cupone["ErrorCode"] == 129:
            par = get_game_info(id=game_id, param=param)
            if par is not None:
                param = par
            time.sleep(1.5)
            continue
        elif cupone["ErrorCode"] == 130:
            time.sleep(1.5)
            continue
        else:
            response = requests.post('https://melbet.ru/dataLineLive/put_bets_common.php', cookies=cookies, headers=headers,
                                     json=json_data)
            with open("ErrorsFile.txt", "a") as file:
                file.write(f"\nSTANDART BET{response.text}\n")
            cupone = response.json()
            if cupone["ErrorCode"] == 0:
                balance = cupone["Value"]["Balance"]
                coeffic = cupone["Value"]["Coupon"]["Coef"]
                parameter = cupone["Value"]["Coupon"]["Events"][0]['Param']
                bet_sum = cupone["Value"]["Coupon"]["Summ"]
                id_coup = cupone["Value"]["Id"]
                coup = {f"{id_coup}": {"balance": balance,
                                       "full_balance": balance + bet_sum,
                                       "coef": coeffic,
                                       "parameter": parameter,
                                       "match_result": 0,
                                       "bet_sum": bet_sum,
                                       "bet_true": 0
                                       }}
                with open("coupones.json", "r") as coupones_file:
                    new_coup = json.load(coupones_file)
                    new_coup.update(coup)
                with open("coupones.json", "w") as coup_file:
                    json.dump(new_coup, coup_file, sort_keys=True, indent=20, ensure_ascii=False)

                break

def standart_or_dogon() -> list or dict:
    with open("coupones.json", "r") as coupones_file:
        all_coups = json.load(coupones_file)
    for coup in all_coups.keys():
        if coup != "user_id":
            if (all_coups[coup]["match_result"] != 0) and (all_coups[coup]["bet_true"] == 1):
                to_dogon = (coup, all_coups.pop(coup))
                return to_dogon
    return ["standart"]

def summ_bet_for_dogon(to_dogon: tuple) -> int:
    with open("balance.json", "r") as balance_file:
        balance = json.load((balance_file))
    balance_now = balance["balance"]
    percentage = {"1": 600,
                  "2": 1200,
                  "3": 1800}
    summ_bet = round(percentage[str(to_dogon[1]['match_result'])])
    if summ_bet < 15:
        summ_bet = 10
        return summ_bet
    elif 1000 > summ_bet >= 15:
        summ_bet = int_r(summ_bet / 10)
        return summ_bet * 10
    elif 10000 > summ_bet >= 1000:
        summ_bet = int_r(summ_bet / 100)
        return summ_bet * 100
    elif summ_bet >= 10000:
        summ_bet = int_r(summ_bet / 1000)
        return summ_bet * 1000

def dogon_bet(user_id: int, uhash: str, game_id: int,param: float, summ: int, to_dogon: tuple):
    cookies = {
        'lng': 'ru',
        '_ga_X2B11TMFNG': 'GS1.1.1655415999.40.1.1655416143.0',
        '_ga': 'GA1.1.1800826200.1655415999',
        'cfdata': 'b99ea673f776af3a164b1fc382c8144a%2500c5eb647939e2bdc75a676d261a7929',
        'cur': 'RUB',
        'login_tries': '0',
        'tzo': '3',
        'ua': f'{user_id}',
        'uhash': f'{uhash}',
        'zsh': '1',
        'sh.session_be98639c': 'c9639afe-7134-489c-93a4-87a3453393de',
        'SESSION': 'ea33ab8af26e5e4b199366a2d9a5bf37',
        'geocountry': 'ru',
        'auid': 'F2nvfGKORnNfC2RTvTZbAg==',
    }

    flag = 0

    headers = {
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'If-Modified-Since': 'Sat, 1 Jan 2000 00:00:00 GMT',
        'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With',
        'Accept-Language': 'ru',
        'Cache-Control': 'no-cache',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'melbet.ru',
        'Origin': 'https://melbet.ru',
        # 'Content-Length': '278',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Referer': 'https://melbet.ru/live/basketball/2288083-belarus-sky-league/380935199-piranhas-astronauts/',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'lng=ru; _ga_X2B11TMFNG=GS1.1.1655415999.40.1.1655416143.0; _ga=GA1.1.1800826200.1655415999; cfdata=b99ea673f776af3a164b1fc382c8144a%2500c5eb647939e2bdc75a676d261a7929; cur=RUB; login_tries=0; tzo=3; ua=413020545; uhash=3080cec956f1d84c9e5362d8528229bd; zsh=1; sh.session_be98639c=c9639afe-7134-489c-93a4-87a3453393de; SESSION=cb78ea4e61ee50f0e635b358560d6a50; geocountry=ru; auid=F2nvfGKORnNfC2RTvTZbAg==',
        'X-Requested-With': 'XMLHttpRequest',
    }

    for i in range(33):
        json_data = {
            'UserId': user_id,
            'Events': [
                {
                    'GameId': game_id,
                    'Type': 9,
                    'Coef': 1.9,
                    'Param': param,
                    'PlayerId': 0,
                    'Kind': 1,
                    'Expired': 0,
                    'Price': 0,
                    'InstrumentId': 0,
                    'Seconds': 0,
                },
            ],
            'partner': 8,
            'Summ': summ,
            'Lng': 'ru',
            'Vid': 0,
            'hash': f'{uhash}',
            'Source': 5,
            'CheckCf': 2,
            'Live': True,
        }

        response = requests.post('https://melbet.ru/dataLineLive/put_bets_common.php', cookies=cookies, headers=headers,
                                 json=json_data)
        with open("ErrorsFile.txt", "a") as file:
            file.write(f"\nDOGON BET{response.text}\n")
        cupone = response.json()
        if cupone["ErrorCode"] == 0:
            old_balance = to_dogon[1]["full_balance"]
            match_res = to_dogon[1]["match_result"]
            balance = cupone["Value"]["Balance"]
            coeffic = cupone["Value"]["Coupon"]["Coef"]
            parameter = cupone["Value"]["Coupon"]["Events"][0]['Param']
            bet_sum = cupone["Value"]["Coupon"]["Summ"]
            id_coup = cupone["Value"]["Id"]
            coup = {f"{id_coup}": {"balance": balance,
                                   "full_balance": old_balance,
                                   "coef": coeffic,
                                   "parameter": parameter,
                                   "match_result": match_res+1,
                                   "bet_sum": bet_sum,
                                   "bet_true": 0
                                   }}
            with open("coupones.json", "r") as coupones_file:
                new_coup = json.load(coupones_file)
                new_coup.update(coup)
                new_coup.pop(to_dogon[0])
            with open("coupones.json", "w") as coupones_file:
                json.dump(new_coup, coupones_file, sort_keys=True, indent=20, ensure_ascii=False)

            break
        elif cupone["ErrorCode"] in [131, 135]:
            time.sleep(1.5)
            continue
        elif cupone["ErrorCode"] == 129:
            par = get_game_info(id=game_id, param=param)
            if par is not None:
                param = par
            time.sleep(1.5)
            continue
        elif cupone["ErrorCode"] == 130:
            time.sleep(1.5)
            continue
        else:
            response = requests.post('https://melbet.ru/dataLineLive/put_bets_common.php', cookies=cookies, headers=headers,
                                     json=json_data)
            with open("ErrorsFile.txt", "a") as file:
                file.write(f"\nDOGON BET{response.text}\n")
            cupone = response.json()
            if cupone["ErrorCode"] == 0:
                old_balance = to_dogon[1]["full_balance"]
                match_res = to_dogon[1]["match_result"]
                balance = cupone["Value"]["Balance"]
                coeffic = cupone["Value"]["Coupon"]["Coef"]
                parameter = cupone["Value"]["Coupon"]["Events"][0]['Param']
                bet_sum = cupone["Value"]["Coupon"]["Summ"]
                id_coup = cupone["Value"]["Id"]
                coup = {f"{id_coup}": {"balance": balance,
                                       "full_balance": old_balance,
                                       "coef": coeffic,
                                       "parameter": parameter,
                                       "match_result": match_res+1,
                                       "bet_sum": bet_sum,
                                       "bet_true": 0
                                       }}
                with open("coupones.json", "r") as coupones_file:
                    new_coup = json.load(coupones_file)
                    new_coup.update(coup)
                    new_coup.pop(to_dogon[0])
                with open("coupones.json", "w") as coupones_file:
                    json.dump(new_coup, coupones_file, sort_keys=True, indent=20, ensure_ascii=False)

                break

def bot_module(game_id: int, param: float):
    try:
        uLogin = config('LOGIN')
        uPassword = config('PASSWORD')
        auth = auth_bet(uLogin=uLogin, uPassword=uPassword)
        user_id = auth[0]
        uhash = auth[1]
        checked_cupones = check_cupones(user_id=user_id, uhash=uhash)
        with open("ErrorsFile.txt", "a") as file:
            file.write(f"\nchecked_cupones\n{checked_cupones}\n")
        balance_update(user_id=user_id, uhash=uhash, cupones_res=checked_cupones)
        to_do = standart_or_dogon()
        with open("ErrorsFile.txt", "a") as file:
            file.write(f"\nSTANDART OR DOGON\n{to_do}\n")
        if to_do == ["standart"]:
            summ = summ_bet_for_stadart()
            with open("ErrorsFile.txt", "a") as file:
                file.write(f"\nSUMM STANDART BET{summ}\n")
            standart_bet(user_id=user_id, uhash=uhash, game_id=game_id, param=param, summ=summ)
        else:
            summ = summ_bet_for_dogon(to_dogon=to_do)
            with open("ErrorsFile.txt", "a") as file:
                file.write(f"\nSUMM DOGON BET{summ}\n")
            dogon_bet(user_id=user_id, uhash=uhash, game_id=game_id, param=param, summ=summ, to_dogon=to_do)
    except Exception:
        pass

def get_game_info(id: int,param: float):
    cookies = {
        'lng': 'ru',
        '_ga_X2B11TMFNG': 'GS1.1.1653688549.14.1.1653690654.0',
        'fixedFooter': '1',
        'unfixedRight': '1',
        '_ga': 'GA1.1.597545221.1653491319',
        'geocountry': 'ru',
        'tzo': '3',
        'SESSION': '921aadedc7c46e39eea1154512ba0f64',
        'sh.session_be98639c': '2dbeebf1-c7f9-49d9-b3d3-5313f2e51244',
        'auid': 'F2nvfGKORnNfC2RTvTZbAg==',
    }

    headers = {
        'Pragma': 'no-cache',
        'Accept': '*/*',
        'If-Modified-Since': 'Sat, 1 Jan 2000 00:00:00 GMT',
        'Accept-Language': 'ru',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Host': 'melbet.ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://melbet.ru/line/basketball/',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'lng=ru; _ga_X2B11TMFNG=GS1.1.1653688549.14.1.1653690654.0; fixedFooter=1; unfixedRight=1; _ga=GA1.1.597545221.1653491319; geocountry=ru; tzo=3; SESSION=921aadedc7c46e39eea1154512ba0f64; sh.session_be98639c=2dbeebf1-c7f9-49d9-b3d3-5313f2e51244; auid=F2nvfGKORnNfC2RTvTZbAg==',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'id': f'{id}',
        'partner': '195',
    }

    try:
        response = requests.get('https://melbet.ru/LiveFeed/GetGameZip', params=params, cookies=cookies, headers=headers)
    except Exception:
        return None
    try:
        stock = response.json()
        val_stock = stock["Value"]
        needed_totals = [(tot["P"], tot["C"]) for _, tot in enumerate(val_stock["E"])
                         if tot["T"] in [9]]
        needed_totals = sorted(needed_totals)
        param_and_coef = needed_totals[-1]
        try:
            if param > param_and_coef[0]:
                param = param_and_coef[0]
                coef = param_and_coef[1]
                if float(coef) >= 1.9:
                    return param
                else:
                    return None
            else:
                return None
        except Exception:
            return None
    except Exception:
        return None

def balance_checker(user_id: int, uhash: str) -> float:
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
    balance_json = response.json()
    balance_from_site = balance_json["balance"][0]["money"]
    return balance_from_site


