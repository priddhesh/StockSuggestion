from bs4 import BeautifulSoup 
import requests
import time
import smtplib
import ssl
from string import Template

choice = int(input("Select 1.NSE 2.BSE\n"))
user_email = input("Enter your e-mail ID to recieve notifications:\n")
company_name = input("Enter company name\n")
company_name = company_name.upper().replace(".","").replace(" ","")
expected_price = float(input("Enter expected price to sell the share\n"))

def stock_suggestion(company,price,id):
 if(choice ==1) :
   html_text = requests.get("https://money.rediff.com/companies/market-capitalisation/nse").text
 else :
   html_text = requests.get("https://money.rediff.com/companies/market-capitalisation").text
 soup = BeautifulSoup(html_text, 'lxml')
 k=0
 a=0
 b=0
 c=0
 d=0
 information = []
 accouncement = []
 str = ""
 str1 = ""
 stock_names = soup.find_all('td', class_="")
 for stock_name in stock_names :
     k=k+1
     if k%7 == 1 :
      name = stock_name.find('a', class_="")
      if name.text.upper().strip().replace(".","").replace(" ","")==company :
       company = name.text.strip()
       link = stock_name.find('a', href = True)
       link = link['href']
       html_link = requests.get("http:"+link).text
       soup = BeautifulSoup(html_link,'lxml')
       high_low = soup.find('span', { "id" : "highlow_nse" })
       high_low = high_low.text
       previous_close = soup.find('span',{"id" : "PrevClose_nse"})
       previous_close = previous_close.text
       high_low_bse = soup.find('span', { "id" : "highlow" })
       high_low_bse = high_low_bse.text
       previous_close_bse = soup.find('span',{"id" : "PrevClose"})
       previous_close_bse = previous_close_bse.text
       HL = soup.find('span',{"id" : "FiftyTwoHighlow_nse"})
       HL = HL.text
       HL_bse = soup.find('span', {"id" : "FiftyTwoHighlow"})
       HL_bse = HL_bse.text
       news = soup.find_all('div', class_="")
       check = soup.find('h2', class_="f14 bold")
       check = check.text
       accs = soup.find_all("a", class_="")
       if "Announcements" not in check :
        for new in news :
          if c>=14 and c<=16 : 
           info = new.find('a', {'rel' : 'nofollow'})
           information.append(info.text)
          c=c+1
        for i in information :
           str += i
           str+="\n"
       else :
        for acc in accs :
          if d==17 or d==19 : 
            accouncement.append(acc.text)
          d=d+1 
        for j in accouncement :
          str1 += j
          str1+="\n"     
       a=k+1
       break
      else :
        continue 

 for stock_name in stock_names :
        b=b+1 
        if b==a:
            stock_price = stock_name.text.replace(",","")
 if float(stock_price)>= price :
  if choice == 1:
     if "Announcements" not in check :
       t = Template('''The price of the stock $stock in NSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close   
Today's High/Low(Rs.) : $high_low     
52wk H/L (Rs.) : $HL  
Realtime news for $stock : 
$str Link : https:$link''')
     else :
       t = Template('''The price of the stock $stock in NSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close   
Today's High/Low(Rs.) : $high_low     
52wk H/L (Rs.) : $HL  
Link : https:$link''')
  else :
     if "Announcements" not in check :
        t = Template('''The price of the stock $stock in BSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close_bse 
Today's High/Low(Rs.) : $high_low_bse
52wk H/L (Rs.) : $HL_bse  
Realtime news for $stock : 
$str Link : https:$link''')   
     else :
        t = Template('''The price of the stock $stock in BSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close_bse  
Today's High/Low(Rs.) : $high_low_bse     
52wk H/L (Rs.) : $HL_bse
BSE Announcements from $stock :
$str1
Link : https:$link''')
  s = t.substitute(stock=company, stock_price=float(stock_price),link = link, high_low = high_low, previous_close=previous_close, high_low_bse= high_low_bse, previous_close_bse=previous_close_bse,HL=HL,HL_bse=HL_bse,str = str,str1=str1)
  a = Template('$email')
  e = a.substitute(email=id)
  print(s)
  ctx = ssl.create_default_context()
  password = "rlvhxiqrigparyok" 
  sender = "riddheshpatil.jee@gmail.com"  
  receiver = e
  message = s
  with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message)
 else :
  if choice == 1:
    if "Announcements" not in check :
      t = Template('''The price of the stock $stock in NSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close 
Today's High/Low(Rs.) : $high_low  
52wk H/L (Rs.) : $HL  
Realtime news for $stock : 
$str Link : https:$link''') 
    else :
       t = Template('''The price of the stock $stock in NSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close   
Today's High/Low(Rs.) : $high_low     
52wk H/L (Rs.) : $HL  
Link : https:$link''') 
  else :
    if "Announcements" not in check :
       t = Template('''The price of the stock $stock in BSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close_bse
Today's High/Low(Rs.) : $high_low_bse  
52wk H/L (Rs.) : $HL_bse  
Realtime news for $stock : 
$str Link : https:$link''')  
    else :
        t = Template('''The price of the stock $stock in BSE market is Rs.$stock_price
Previous Close(Rs.) : $previous_close_bse   
Today's High/Low(Rs.) : $high_low_bse     
52wk H/L (Rs.) : $HL_bse 
BSE Announcements from $stock :
$str1
Link : https:$link''')
  s = t.substitute(stock=company, stock_price=float(stock_price),link = link, high_low = high_low, previous_close= previous_close,high_low_bse = high_low_bse, previous_close_bse=previous_close_bse,HL_bse = HL_bse,HL=HL,str = str,str1=str1)
  print(s)           

if __name__ == "__main__" :
    while True :
        stock_suggestion(company_name,expected_price,user_email)
        time_wait = 5
        print(f'Waiting {time_wait} minutes....')
        time.sleep(time_wait*60)

    
