import json
import requests
import subprocess

base_url = "https://demo92.visual-host.com/api/"

dashboard_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',  # نوع المحتوى
    'Authorization': 'Bearer 2|ASAuZhU3p1PHeLOfteuXWR6KTuPuaqsDk4h9hfEb01914cf0'  # معلومات المصادقة مع access token
}



async def ichancyWithdraw(user_id,playerId,amount,context):
    
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
    "amount": -int(amount),
    "comment": None,
    "playerId": playerId,
    "currencyCode": "NSP",
    "currency": "NSP",
    "moneyStatus": 5
    }
    passed = False
    while not passed:
        response = requests.post("https://agents.ichancy.com/global/api/Player/withdrawFromPlayer",json=body,headers=headers)
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
            if result==False:
                passed=True
                return {"status":"InsuffBalance","message":"⛔️ لايوجد رصيد كافي في حسابك أيشانسي لسحب المبلغ المطلوب"}
            if result == "ex":
                data1 = '{"username": "Brhoom@agent.nsp","password": "Bas889@@"}'
                response = requests.post("https://agents.ichancy.com/global/api/User/signIn",data=data1,headers=headers)
                print("________________________")
                print(response.status_code)
                print(response.json())
            else:
                passed = True
                break
    if passed:
        print("------success withdraw ichancy-----")
        response = requests.post(base_url+"successWithdrawchancy",json={"chat_id":user_id,"amount":amount,"type":"withdraw"},headers=dashboard_headers)
        if response.status_code== 200:
            response_json = response.json()
            print(response_json)
            return response_json
        else:
            return {"status":"failed","message":"تم شحن حسابك بنجاح، لكن فشل تسجيل العملية في البوت"}
                
    else:
        print("------failed charge ichancy-----")
        return {"status":"failed","message":"حدث خطأ أثناء شحن حساب أيشانسي، الرجاء المحاولة مرة أخرى"}

