import json
import requests

def get_champ_match_id(id):
    cookies = {
        '_ga_X2B11TMFNG': 'GS1.1.1653688549.14.1.1653689155.0',
        'lng': 'ru',
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
        'Referer': 'https://melbet.ru/live/',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '_ga_X2B11TMFNG=GS1.1.1653688549.14.1.1653689155.0; lng=ru; fixedFooter=1; unfixedRight=1; _ga=GA1.1.597545221.1653491319; geocountry=ru; tzo=3; SESSION=921aadedc7c46e39eea1154512ba0f64; sh.session_be98639c=2dbeebf1-c7f9-49d9-b3d3-5313f2e51244; auid=F2nvfGKORnNfC2RTvTZbAg==',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'lng': 'ru',
        'champ': f'{id}',
        'partner': '195',
        'tf': '1000000',
    }
    try:
        response = requests.get('https://melbet.ru/LiveFeed/GetChampZip', params=params, cookies=cookies, headers=headers)
        # Операции с сохранением json
        with open("live/get_champ_zip_live_json.json", "w") as file:
            file.write(response.text)
        with open("live/get_champ_zip_live_json.json") as f:
            temp = json.load(f)
        with open('live/get_champ_zip_live_json.json', 'w') as f:
            json.dump(temp, f, sort_keys=True, indent=20, ensure_ascii=False)
        # Достаем информацию из json
        with open('live/get_champ_zip_live_json.json') as file:
            stock = json.load(file)

        val_stock = stock["Value"]["G"]
        # Достаем матч id
        ids_matchs = list()
        for _, match in enumerate(val_stock):
            ids_matchs.append(match["I"])
    except Exception:
        return None
    return ids_matchs
