import requests
from teamdetails import team
from datetime import datetime
import smtplib
import ssl
from email.message import EmailMessage
import multiprocessing
from dotenv import load_dotenv
import os
import pytz


load_dotenv()
EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TOKEN = os.getenv("TOKEN")
CLIENT_MAIL = os.getenv("CLIENT_MAIL")


def send_mail(email_receiver, subject, body):
    email_sender = f"{EMAIL_ID}"
    password = f"{EMAIL_PASS}"
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as connection:
        connection.login(email_sender, password)
        connection.sendmail(email_sender, email_receiver, em.as_string())


def send_message(set_time, cid, expiry_date):
    print("started")
    while datetime.now().strftime("%Y-%m-%d") != expiry_date:
        send_url = "https://discord.com/api/v9/channels/{}/messages"
        send_payload = {
            'content': f"{team}"
        }
        send_header = {
            "authorization": f"{TOKEN}"
        }
        issent = True
        checktime = True
        while checktime:
            tz_NY = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(tz_NY).strftime("%H:%M:%S")
            if current_time == set_time or True:
                while issent:
                    response = requests.post(send_url.format(cid), data=send_payload, headers=send_header)
                    if len(response.json()) < 5:
                        continue
                    else:
                        issent = False
                        checktime = False
                        print("Message sent successfully!")


def receive_message(set_time, number, cid, expiry_date):
    while datetime.now().strftime("%Y-%m-%d") != expiry_date:
        current_date = datetime.now().strftime("%Y:%m:%d")
        recv_url = f"https://discord.com/api/v9/channels/{cid}/messages?limit=50"
        recv_header = {
            "authorization": f"{TOKEN}"
        }
        global rchecktime, isrecv, contents
        isrecv = True
        rchecktime = True
        contents = []
        while rchecktime:
            tz_NY = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(tz_NY).strftime("%H:%M:%S")
            if current_time == set_time:
                while isrecv:
                    recv_response = requests.get(recv_url, headers=recv_header)
                    try:
                        for i in range(number):
                            timestamp = recv_response.json()[i]['timestamp'][0:10]
                            req_date = timestamp.replace("-", ":")
                            if current_date == req_date:
                                content = recv_response.json()[i]['content']
                                isrecv = False
                                rchecktime = False
                                contents.append(content)
                            else:
                                rchecktime = False
                    except KeyError:
                        rchecktime = False
                        x = "Channel not available!\nCheck the particular discord server!"
                        subject = "Alert"
                        body = f"""\n
                                                    {x}
                                                    """
                        send_mail(f"{CLIENT_MAIL}", subject=subject, body=body)
                        print("Alert-Mail Sent!")
                        isrecv = False
                    except IndexError:
                        rchecktime = False
                        pass
        if contents != []:
            res = ' \n'.join(contents)
            print(res)
            print("ID PASS Received")
            subject = "ID Pass"
            body = f"""\n
                                {res}
                                """
            send_mail(f"{CLIENT_MAIL}", subject=subject, body=body)
            print("Success-Mail Sent!")

contents = []
# send_message("13:57:00", "991611117518454784")
# receive_message("14:53:00", 1, "710080535116120080")

p1 = multiprocessing.Process(target=send_message, args=("13:59:00", "829649127415480360", "2022-07-13"))
p2 = multiprocessing.Process(target=send_message, args=("14:00:00", "839432708446355507", "2022-07-13"))
p3 = multiprocessing.Process(target=send_message, args=("14:01:00", "839429244853420062", "2022-07-13"))
p4 = multiprocessing.Process(target=send_message, args=("14:02:00", "839429137365205022", "2022-07-13"))
p5 = multiprocessing.Process(target=send_message, args=("14:03:00", "822727877845057587", "2022-07-13"))
p6 = multiprocessing.Process(target=send_message, args=("14:04:00", "790865110787948584", "2022-07-13"))
p7 = multiprocessing.Process(target=send_message, args=("14:05:00", "790865151313707029", "2022-07-13"))
p8 = multiprocessing.Process(target=send_message, args=("14:06:00", "790865190916456479", "2022-07-13"))


if __name__ == '__main__':
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
