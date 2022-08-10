import requests
import json


from live.get_sports_live import get_leagues_id_live as league
from live.get_champs_live import get_champ_match_id as match_id
from db_match.database_creation import show_info
from db_match.database_creation import add_info
from betbot.betbot import bot_module







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
        response = requests.get('https://melbet.ru/LiveFeed/GetGameZip', params=params, cookies=cookies, headers=headers)
    except Exception:
        return None
    try:
        with open("live/get_gamelive.json", "w") as file:
            file.write(response.text)
        with open("live/get_gamelive.json") as f:
            temp = json.load(f)
        with open('live/get_gamelive.json', 'w') as f:
            json.dump(temp, f, sort_keys=True, indent=20, ensure_ascii=False)
        # Достаем информацию из json
        with open('live/get_gamelive.json') as file:
            stock = json.load(file)
        val_stock = stock["Value"]
        game_id = val_stock["I"]
        game_all_totals = [(tot["P"], tot["T"], tot["C"]) for _, tot in enumerate(val_stock["E"])
                           if tot["T"] in [10, 9]]
        game_all_totals = sorted(game_all_totals)
        needed_totals = [(tot["P"], tot["C"]) for _, tot in enumerate(val_stock["E"])
                         if tot["T"] in [9]]
        needed_totals = sorted(needed_totals)
        need_total = str()
        for _, tota in enumerate(needed_totals):
            need_total += f"{tota[0]}Б КФ {tota[1]}\n"
        b = list()
        for i in range(0, len(game_all_totals), 2):
            if game_all_totals[i][0] == game_all_totals[1 + i][0]:
                b.append((game_all_totals[i][0], round(abs(game_all_totals[i][2] - game_all_totals[1 + i][2]), 3)))
        find_totalscoef_list = list(map(lambda x: min(x), b))
        if len(find_totalscoef_list) > 0:
            min_total = game_all_totals[0][0]
            param_and_coef = list()
            for _, tota in enumerate(needed_totals):
                if round(tota[0], 1) == round(min_total+9, 1):
                    param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 8, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 7, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 6, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 5, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 4, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 3, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 2, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total + 1, 1):
                        param_and_coef = tota
            if len(param_and_coef) == 0:
                for _, tota in enumerate(needed_totals):
                    if round(tota[0], 1) == round(min_total, 1):
                        param_and_coef = tota


            try:
                    with open("buffer_game_id.json") as file:
                        buf = json.load(file)
                    if str(game_id) not in buf.keys():
                        buf.update({f"{game_id}": {"-20": False,
                                                   "-23": False}})
                    with open("buffer_game_id.json", 'w') as file:
                        json.dump(buf, file, sort_keys=True, indent=20, ensure_ascii=False)
                    prematch_data = show_info(home_id=val_stock['O1I'], guest_id=val_stock['O2I'], liga_id=val_stock['LI'])
                    fix = float(prematch_data[8])
                    upd_total = round(float(prematch_data[12]), 2)
                    if buf[str(game_id)]["-23"] == False:
                        if round(fix * 0.77, 1) >= min_total and\
                                round(fix * 0.6, 1) < min_total and\
                                (upd_total == 0 or upd_total >= round(fix * 0.77, 1)):
                            try:
                                add_info(column="total_min", value=min_total, game_id=int(prematch_data[0]))
                                test = show_info(home_id=val_stock['O1I'], guest_id=val_stock['O2I'], liga_id=val_stock['LI'])
                                if round(float(test[12]), 1) != min_total:
                                    raise Exception
                            except Exception:
                                return None

                            # try:
                            #     param = param_and_coef[0]
                            #     bot_module(param=param, game_id=game_id)
                            # except Exception:
                            #     pass

                            prematch_data[12] = f"Минимальный тотал сейчас: {min_total} -23%\n" \
                                                f"Игровая минута:{val_stock['SC']['TS'] // 60}\n\n" \
                                                f"{need_total}"
                            buf[str(game_id)]["-23"] = True
                            buf[str(game_id)]["-20"] = True
                            with open("buffer_game_id.json", 'w') as file:
                                json.dump(buf, file, sort_keys=True, indent=20, ensure_ascii=False)
                            return prematch_data
                    if buf[str(game_id)]["-20"] == False:
                        if round(fix * 0.8, 1) >= min_total and\
                                round(fix * 0.6, 1) < min_total and\
                                (upd_total == 0 or upd_total >= round(fix * 0.8, 1)):
                            try:
                                add_info(column="total_min", value=min_total, game_id=int(prematch_data[0]))
                                test = show_info(home_id=val_stock['O1I'], guest_id=val_stock['O2I'], liga_id=val_stock['LI'])
                                if round(float(test[12]), 1) != min_total:
                                    raise Exception
                            except Exception:
                                return None

                            # try:
                            #     param = param_and_coef[0]
                            #     bot_module(param=param, game_id=game_id)
                            # except Exception:
                            #     pass

                            prematch_data[12] = f"Минимальный тотал сейчас: {min_total} -20%\n" \
                                                f"Игровая минута:{val_stock['SC']['TS'] // 60}\n\n" \
                                                f"{need_total}"
                            buf[str(game_id)]["-20"] = True
                            buf[str(game_id)]["-23"] = True
                            with open("buffer_game_id.json", 'w') as file:
                                json.dump(buf, file, sort_keys=True, indent=20, ensure_ascii=False)
                            return prematch_data

            except Exception:
                return None
    except Exception:
        return None


def find_all_games_live():
    try:
        all_signals = list()
        leagues = league()
        for _, liga in enumerate(leagues):
            for indx, id in enumerate(match_id(liga[1])):
                if id == None:
                    continue
                signal = get_game_info(id)
                all_signals.append(signal)
    except Exception:
        return None
    return all_signals
