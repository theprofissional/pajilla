import requests
import time
from datetime import datetime
from telegram import Bot

# بيانات الاعتماد
API_KEY = '465cb9a7996b73f37d9f33d5f39d5fb1'
TELEGRAM_TOKEN = '7821483378:AAGd0FoOpnbncAhhHAvtHCNgeKdmOOArmmQ'
CHAT_ID = '1718690258'

bot = Bot(token=TELEGRAM_TOKEN)

def get_today_matches():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json().get('response', [])

def is_suspicious(match_stats):
    try:
        over_25_home = match_stats['home']['statistics']['goals']['avg']['total'] > 2.5
        under_15_away = match_stats['away']['statistics']['goals']['avg']['total'] < 1.5
        btts_yes = match_stats['both_teams_to_score'] == 'yes'
        return over_25_home and under_15_away and btts_yes
    except:
        return False

def get_match_stats(fixture_id):
    url = f"https://v3.football.api-sports.io/teams/statistics?fixture={fixture_id}"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def monitor_matches():
    matches = get_today_matches()
    suspicious_matches = []

    for match in matches:
        fixture_id = match['fixture']['id']
        home = match['teams']['home']['name']
        away = match['teams']['away']['name']
        date = match['fixture']['date']

        try:
            stats = get_match_stats(fixture_id)
            if is_suspicious(stats):
                suspicious_matches.append((home, away, date))
        except:
            continue

    if suspicious_matches:
        for match in suspicious_matches:
            home, away, date = match
            message = f"⚠️ مباراة مشبوهة ⚠️\n{home} vs {away}\nالتاريخ: {date[:10]}\nتحليل: تم اكتشاف إحصائيات غير طبيعية."
            bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        print("لا توجد مباريات مشبوهة اليوم.")

while True:
    try:
        monitor_matches()
    except Exception as e:
        print("خطأ:", e)
    time.sleep(3600)  # كل ساعة
