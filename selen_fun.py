from seleniumbase import SB
import requests


def ichancyFun():
    status_code = (requests.get("https://agents.ichancy.com/")).status_code
    

def get_cookies_and_user_agent():
    with SB(uc=True) as sb:
        url = "https://agents.ichancy.com/"
        sb.activate_cdp_mode(url)
        sb.uc_gui_click_captcha()
        sb.sleep(10)
        sb.wait_for_ready_state_complete(timeout=60)
       
        driver = sb.driver
        session_id = driver.session_id
        cookies = driver.get_cookies()
    
        user_agent = driver.execute_script("return navigator.userAgent;")
        cookies_text = ""
        for cookie in cookies:
            cookies_text += f"{cookie['name']}={cookie['value']};"
    return cookies_text, user_agent

cookies, user_agent = get_cookies_and_user_agent()
print(cookies+"+basel+"+user_agent)
