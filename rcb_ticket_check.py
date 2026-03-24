import os
import requests
from twilio.rest import Client
import time
import json
import logging

# RAILWAY ENVIRONMENT VARIABLES
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN') 
CONTENT_SID = os.getenv('CONTENT_SID')
YOUR_PHONE = os.getenv('PHONE')

client = Client(account_sid, auth_token)
logging.basicConfig(filename='/tmp/rcb_tickets.log', level=logging.INFO)

print("🚀 RCB TICKET MONITOR v2.0 - RAILWAY 24/7")
print("⏳ Precise triggers only")

def check_tickets():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    urls = ["https://shop.royalchallengers.com/ticket", "https://www.royalchallengers.com"]
    
    all_text = ""
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"  → {url} ({resp.status_code})")
            all_text += resp.text.lower()
        except:
            print(f"  → {url} (error)")
    
    precise_triggers = ['book now', 'book tickets', 'select seats', 'choose your seats']
    false_positives = ['ticketgenie', 'coming soon']
    
    found = [t for t in precise_triggers if t in all_text]
    has_false = any(fp in all_text for fp in false_positives)
    
    if found and not has_false:
        print(f"✅ REAL TICKETS: {found}")
        return True
    return False

def send_alert():
    vars = json.dumps({"1": "🚨 RCB vs SRH LIVE!", "2": "shop.royalchallengers.com NOW!"})
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        content_sid=CONTENT_SID,
        content_variables=vars,
        to=YOUR_PHONE
    )
    print(f"✅ WHATSAPP: {message.sid}")
    return True

check_count = 0
try:
    while True:
        check_count += 1
        print(f"\n[{check_count}] {time.strftime('%H:%M:%S')}")
        if check_tickets():
            send_alert()
            break
        print("⏳ 30s...")
        time.sleep(30)
except:
    pass
