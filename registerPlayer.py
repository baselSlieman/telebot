import json
import random
import sqlite3
import string
import requests
import subprocess

base_url = "https://demo92.visual-host.com/api/"

dashboard_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',  # نوع المحتوى
    'Authorization': 'Bearer 2|ASAuZhU3p1PHeLOfteuXWR6KTuPuaqsDk4h9hfEb01914cf0'  # معلومات المصادقة مع access token
}
# email = "asdxxasxerw@agent.nsp"
# ich_username = "bas2e2elsd123"
# ich_password = "as2dasd123"
# user_id=1111111

# cookies = "languageCode=en_GB;PHPSESSID_3a07edcde6f57a008f3251235df79776a424dd7623e40d4250e37e4f1f15fadf=cfff69f67e2d841314cb9fa0bbd4045d;language=English%20%28UK%29;cf_clearance=bA8jKpPu4UwZfVpzlCMXp.QN53SX9NRJ5nW3SvcTZZg-1746919236-1.2.1.1-Qp3.kZGhBV_mctVw3RcgJy1w9Op4E9A15v_VS4E01jzi8PVCAs4YWDp3TiVbDwIYOExdTKLIMfF_9K7wtLIdn3jTJ6fKfgEejechlp57fjosQj5RStMJwqPKt3E.br.5xc9vAEKT7hwS9CiaMf8DmI9ltiFuzFCAgqglJ0GOOzPXHljTRjKiLSuzyd.HOJKbb2hgyNuzRthdCEaJmRQm1LweIJgGGzNYYDr6CPxtdgCTP3iFqSYmORQBvXFycDAwsXGUn6IwffActLcRQf98sSXMvSKtyegpUYb9IrsYfb1N7qR11sJMH88JBv.F2yKxpHH4QTY4yXa3BfFvCHiMocL9zzxxzHzNnNfpr0Yvh4MN4nKxXjhAQmrWcqjpzD.5;__cf_bm=jDfkO.tDSRHhzLWSe9FeY0cVfgTWGW9SayX.lPWcb5E-1746919229-1.0.1.1-4cJHstwZ5QU9JbguCzdsZFlNtYxgZACgLyCtkPZtznbEkoZn7JgOmQCWiPo_VpQqwdct8WgFhC6225l81E_rByH14Cq5n5P7l8cdLo6Mr0g"
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"


async def register_player(user_id,ich_username, ich_password,context):
    emailExt = "@player.nsp"
    email = ich_username+emailExt
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
    # data={
    #     "player":f'{"email":"{email}","password":"{ich_password}","parentId":"2344226","login":"{ich_username}"}'
    # }

    body = {
        "player": {
            "email": email,
            "password": ich_password,
            "parentId": "2344226",
            "login": ich_username
        }
    }
    passed = False
    while not passed:
        response = requests.post("https://agents.ichancy.com/global/api/Player/registerPlayer",json=body,headers=headers)
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
            if result==1:
                passed=True
                break
            if result == "ex":
                data1 = '{"username": "Brhoom@agent.nsp","password": "Bas889@@"}'
                response = requests.post("https://agents.ichancy.com/global/api/User/signIn",data=data1,headers=headers)
                print("________________________")
                print(response.status_code)
                print(response.json())
                # set_cookie_values = response.headers.get('Set-Cookie')
                # get_cookie_values = response.headers.get('Cookie')
                # print('Set-Cookie: '+set_cookie_values)
                # print(get_cookie_values)
                # cookies = ''
                # for cookie in get_cookie_values:
                #     parts = cookie.split(';')
                #     cookies += parts[0].strip() + ';'
                # cookies = cookies.rstrip(';')
            else:
                chars = ''.join(random.sample(string.ascii_lowercase + string.digits, len(string.ascii_lowercase + string.digits)))
                random_string = ''.join(random.sample(chars, 4))
                ich_username += random_string
                email = ich_username+emailExt
                ich_password += random_string
                body['player']['email']=email
                body['player']['login']=ich_username
                body['player']['password']=ich_password
    if passed:
        print("------success register player-----")
        bodyPlayerID = {
            "start": 0,
            "limit": 20,
            "filter": {},
            "isNextPage": "False",
            "searchBy": {
                "getPlayersFromChildrenLists": ich_username
            }
        }
        print(bodyPlayerID)
        response = requests.post("https://agents.ichancy.com/global/api/Player/getPlayersForCurrentAgent",json=bodyPlayerID,headers=headers)
        if response.status_code==200:
            print(response.json())
            result= (response.json())['result']
            if isinstance(result, dict):
                player_id = result["records"][0]["playerId"]
                print(player_id)
                response = requests.post(base_url+"newichaccount_v3",json={"identifier":player_id,"chat_id":user_id,"e_username":ich_username,"e_password":ich_password},headers=dashboard_headers)
                if response.status_code== 200:
                    response_json = response.json()
                    print(response_json)
                    if response_json["status"] == "success":
                        conn = sqlite3.connect('users.db')
                        c = conn.cursor()
                        c.execute("INSERT INTO ichancy (user_id,username,playerId) VALUES (?,?,?)", (user_id,ich_username,player_id))
                        conn.commit()
                        conn.close()
                    return response_json
                else:
                    return {"status":"failed","message":"حدث خطأ أثناء تخزين بيانات الطلب الرجاء المحاولة مرة أخرى"}
            else:
                return {"status":"failed","message":"حدث خطأ أثناء تخزين معرف اللاعب، الرجاء المحاولة مرة أخرى"}
        else:
            return {"status":"failed","message":"حدث خطأ أثناء تخزين معرف اللاعب، الرجاء المحاولة مرة أخرى"}    
    else:
        print("------failed register player-----")
        return {"status":"failed","message":"حدث خطأ أثناء إنشاء الحساب، الرجاء المحاولة مرة أخرى"}

