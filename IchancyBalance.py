import json
import requests
import subprocess

base_url = "http://localhost:8000/api/"

dashboard_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',  # نوع المحتوى
    'Authorization': 'Bearer 1|JrqSlcvhpxY6Gdv2Wiggyrg7n3Fd8Q16mza8AeArc249fbcf'  # معلومات المصادقة مع access token
}



async def getIchancyBalance(user_id,playerId,context):
    
    with open('data.json', 'r') as file:
        datass = json.load(file)

    cookies = datass.get('cookies', '')
    user_agent = datass.get('user_agent', '')
    headers = {
        'Content-Type' : 'application/json',
        'User-Agent' : user_agent.strip(),
        'Accept-Encoding' : 'gzip,deflate,br',
        'Accept' : '*/*',
        'dnt': '1',
        'origin':'https://agents.ichancy.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-encoding':'gzip, deflate, br',
        'accept-language': 'ar-AE,ar;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
        'cookie' : cookies,
    }
    body = {
    "playerId": playerId,
    }
    passed = False
    while not passed:
        response = requests.post("https://agents.ichancy.com/global/api/Player/getPlayerBalanceById",json=body,headers=headers)
        print(response.status_code)
        if response.status_code == 403:
            await context.bot.send_message(chat_id=user_id, text="شكراً لانتظارك \n سيتم إعلامك بنتيجة العملية خلال دقيقة واحدة على الأكثر")
            process = subprocess.Popen(["python", "selen_fun.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            stdout, stderr = process.communicate()
            lines = (stdout.decode()).split("+basel+")
            cookies = lines[0]
            user_agent = lines[1]
            headers['cookie'] = cookies
            headers['User-Agent'] = user_agent.strip()
            print(cookies)
            print("---------------------------")
            print(user_agent)
            datas = {
                "cookies": cookies,
                "user_agent": user_agent.strip()
            }

            with open('data.json', 'w') as file:
                json.dump(datas, file)
        else:
            print(response.json())
            result= (response.json())['result']
            if isinstance(result, list):
                ichancyBalance = result[0].get("balance", None)
                if ichancyBalance is not None:
                    message = f"🌳 رصيد حساب أيشانسي الخاص بك: {ichancyBalance} NSP"
                    await context.bot.send_message(chat_id=user_id, text=message)
                    return
            if result == "ex":
                data1 = '{"username": "Brhoom@agent.nsp","password": "Bas889@@"}'
                response = requests.post("https://agents.ichancy.com/global/api/User/signIn",data=data1,headers=headers)
                print("________________________")
                print(response.status_code)
                print(response.json())

