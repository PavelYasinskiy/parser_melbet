import json
import requests


def get_leagues_id_live() -> list:
    cookies = {
        'SESSION': '98ec4accd8979a5f488598a469d62559',
        'lng': 'ru',
        'auid': 'F2nvfGJHbfitsV87+M6EAg==',
        'tzo': '3',
        'sh.session_be98639c': '36d0dd58-f03c-4dce-99d9-a8e333ddf4e0',
        'cur': 'RUB',
        'login_tries': '0',
        'zsh': '1',
        'cfdata': '25166e6fa51a6eb1a09537113cf84c60b0',
        'uhash': '335363831bc2706c15a5103cbeec6d85',
        'geocountry': 'ru',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'SESSION=98ec4accd8979a5f488598a469d62559; lng=ru; auid=F2nvfGJHbfitsV87+M6EAg==; tzo=3; sh.session_be98639c=36d0dd58-f03c-4dce-99d9-a8e333ddf4e0; cur=RUB; login_tries=0; zsh=1; cfdata=25166e6fa51a6eb1a09537113cf84c60b0; uhash=335363831bc2706c15a5103cbeec6d85; geocountry=ru',
        'If-Modified-Since': 'Sat, 1 Jan 2000 00:00:00 GMT',
        'Referer': 'https://melbet.ru/line/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.53 (Edition Yx 05)',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'lng': 'ru',
        'champs': '0',
        'partner': '195',
        'tf': '1000000',
        'cyberFlag': '4',
    }
    try:
        response = requests.get('https://melbet.ru/LiveFeed/GetSportsZip', params=params, cookies=cookies, headers=headers)
        # Операции с сохранением json
        with open("live/get_sport_zip_line_json.json", "w") as file:
            file.write(response.text)
        with open("live/get_sport_zip_line_json.json") as f:
            temp = json.load(f)
        with open('live/get_sport_zip_line_json.json', 'w') as f:
            json.dump(temp, f, sort_keys=True, indent=20, ensure_ascii=False)
        # Достаем информацию из json
        with open('live/get_sport_zip_line_json.json') as file:
            stock = json.load(file)
        val_stock = stock["Value"]
        # Достаем вид спорта баскетбол
        for _, sport in enumerate(val_stock):
            if sport["E"] == "Basketball":
                basketball = sport["L"]
        #  Создаем список (название лиги, id лиги)
        bad_ligas_id = [2123242, 2288083, 2105769, 1939157, 1942551,
                        1106653, 1766419, 1204071, 1207381, 2039399,
                        1521087, 1525335, 1315317, 1795519, 1940373,
                        2249894, 2249891, 2401891, 2272568, 2282332,
                        1531223, 1521033, 1525333, 1315319, 1315317,
                        1240637, 877809, 1863620, 2251632, 2227776,
                        2417303, 88693, 1265963, 1266861]
        leagues = [(liga["L"], liga["LI"]) for _, liga in enumerate(basketball)
                   if (liga['LI'] not in bad_ligas_id) and ("3x3" not in liga["L"])]

    except Exception:
        return None
    return leagues