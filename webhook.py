from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

API_KEY = "68fa334fb1msh6f4ec3f3e2f2b92p16fda4jsn09232406a55a"

def get_today_matches():
    today = datetime.date.today().strftime("%Y-%m-%d")  # Отримуємо поточну дату

    url = "https://livescore-football.p.rapidapi.com/soccer/news-detail?slug=mourinho-buys-afena-gyan-800-trainers-after-match-winning-roma-display-2021112223190752865"
    headers = {"x-apisports-key": API_KEY}
    params = {"date": today}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        matches = []
        for match in data['response']:
            league = match['league']['name']
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            time = match['fixture']['date'][11:16]  # Витягуємо лише час
            matches.append(f"{league}: {home} vs {away} о {time}")
        
        if matches:
            return "\n".join(matches)
        else:
            return "Сьогодні матчів немає."
    else:
        return "Не вдалося отримати інформацію про матчі 😢"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    intent_name = req['queryResult']['intent']['displayName']
    
    if intent_name == "who_plays_today":
        matches = get_today_matches()
        return jsonify({
            "fulfillmentText": matches
        })
    
    return jsonify({"fulfillmentText": "Не знаю, що відповісти 😅"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Render вимагає порт від 10000
