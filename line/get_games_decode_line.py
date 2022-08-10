import requests
import json
from line.get_sports_decode_line import get_leagues_id_line as league
from line.get_champs_decode_line import get_champ_match_id as match_id
from db_match import database_creation


def get_game_info(id):
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
        response = requests.get('https://melbet.ru/LineFeed/GetGameZip', params=params, cookies=cookies, headers=headers)

        with open("line/get_game_zip_line_json.json", "w") as file:
            file.write(response.text)
        with open("line/get_game_zip_line_json.json") as f:
            temp = json.load(f)
        with open('line/get_game_zip_line_json.json', 'w') as f:
            json.dump(temp, f, sort_keys=True, indent=20, ensure_ascii=False)
        # Достаем информацию из json
        with open('line/get_game_zip_line_json.json') as file:
            stock = json.load(file)
        val_stock = stock["Value"]
        game_all_totals = [(tot["P"], tot["T"], tot["C"]) for _,tot in enumerate(val_stock["E"]) if tot["T"] in [10, 9]]
        game_all_totals = sorted(game_all_totals)
        b = list()
        for i in range(0, len(game_all_totals),2):
          if game_all_totals[i][0] == game_all_totals[1+i][0]:
            b.append((game_all_totals[i][0], round(abs(game_all_totals[i][2]-game_all_totals[1+i][2]),3)))
        find_totalscoef_list = list(map(lambda x: min(x), b))
        if len(find_totalscoef_list) > 0:
            find_totalscoef_list = find_totalscoef_list.index(min(find_totalscoef_list))
            total_b = game_all_totals[find_totalscoef_list*2]
            total_m = game_all_totals[find_totalscoef_list*2+1]
            database_creation.create_info(val_stock['I'])
            database_creation.add_info(column="liga_eng", value=val_stock['LE'], game_id=val_stock['I'])
            database_creation.add_info(column="liga_ru", value=val_stock['L'], game_id=val_stock['I'])
            database_creation.add_info(column="liga_id", value=val_stock['LI'], game_id=val_stock['I'])
            database_creation.add_info(column="home", value=val_stock['O1'], game_id=val_stock['I'])
            database_creation.add_info(column="home_id", value=val_stock['O1I'], game_id=val_stock['I'])
            database_creation.add_info(column="guest", value=val_stock['O2'], game_id=val_stock['I'])
            database_creation.add_info(column="guest_id", value=val_stock['O2I'], game_id=val_stock['I'])
            database_creation.add_info(column="total_mid_b", value=total_b[0], game_id=val_stock['I'])
            database_creation.add_info(column="total_coef_b", value=total_b[2], game_id=val_stock['I'])
            database_creation.add_info(column="total_mid_m", value=total_m[0], game_id=val_stock['I'])
            database_creation.add_info(column="total_coef_m", value=total_m[2], game_id=val_stock['I'])
            database_creation.add_info(column="total_min", value=0, game_id=val_stock['I'])
    except Exception:
        pass


def find_all_games_line():
    try:
        leagues = league()
        for _, liga in enumerate(leagues):
            for indx, id in enumerate(match_id(liga[1])):
                get_game_info(id)
    except Exception:
        pass
