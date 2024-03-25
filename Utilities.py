from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import smtplib, hashlib, gspread, pandas as pd, threading, qrcode,os
from globalDeclarations import *

password = "your-password"
email = "your-email@gmail.com"
lock = threading.Lock()

# Give path to your file here Auth credentials file generated using GCP Sheets API
servac = gspread.service_account("credentials.json") 

# Enter your Google Sheet's Key here (available in URL of the sheet)
# Your sheet should be public and on editor mode
excel = servac.open_by_key("")

def success(data):
    wks = excel.worksheet("Participants")
    df = pd.DataFrame(wks.get_all_records())

    wks2 = excel.worksheet("Verify")
    df2 = pd.DataFrame(wks2.get_all_records())

    data = dict(data)
    data['email'] = data['email'].lower()
    data['Hex'] = hashfunc(data['email'])
    data['Hexcode'] = str(hashfunc(data['email'])[:5])
    print(data.keys())
    if "id" in data.keys() and "department" in data.keys() and "course" in data.keys() and "section" in data.keys():
        data.pop('id')
        data.pop('department')
        data.pop('course')
        data.pop('section')

    if len(df) > 0:
        vals = df['Hex'].values
        if data['Hex'] in vals:
            return base_url + "already_reg.html"

    lock.acquire()
    try:
        df = pd.DataFrame(wks.get_all_records())
        if len(df) == 0:
            df = pd.DataFrame(data, columns=["name","email","category","comp","Hex","Hexcode","parts","contact","tname"], index=[data])
        else:
            df.loc[len(df)] = data
        
        if len(df2) == 0:
            data["Verified"] = 0
            df2 = pd.DataFrame(data, columns=["name","email","comp","Hexcode","parts","Verified"], index=[data])
        else:
            data["Verified"] = 0
            new_data = {key: data[key] for key in ["name","email","comp","Hexcode","parts","Verified"]}
            df2.loc[len(df2)] = new_data

        wks.update([df.columns.values.tolist()] + df.values.tolist())
        wks2.update([df2.columns.values.tolist()] + df2.values.tolist())
        lock.release()
    except Exception as e:
        print(e)
        lock.release()
    finally:
        pass

    qrgen(data)
    return base_url + "success.html"

def hashfunc(email):
    email_bytes = email.encode('utf-8')
    hash_object = hashlib.sha256(email_bytes)
    hex_digest = hash_object.hexdigest()
    return "A" + hex_digest[:10].upper()


def mailer(data):
    global GCR
    hex_code = hashfunc(data['email'])

    msg = MIMEMultipart()
    msg['From'] = "SYSTEMS LIMITED DEVDAY 2023"
    msg['To'] = data['email']
    msg['Subject'] = "ACM-NUCES DevDay 2023 - Registration CONFIRMED!"

    message=f'''<body style="font-family: Trebuchet MS; line-spacing:1.5rem; font-size: 14px;">Dear {data['name']},<br>
    <br>We are delighted to inform you that your registration for SYSTEM LIMITED DEVDAY 2023 has been successfully confirmed! We appreciate your interest in our event and are thrilled to have you on board.<br>
    <br>Some useful participation information is given below:<br>
    <p style="font-family: Cambria; font-size:16px; line-spacing:2rem; font-weight:400;">Team Name: {data['tname']}<br>Competition: {data['category']}<br>Type: {data['comp']}<br>Number of Participants: {data['parts']}</p>
    <br>As we gear up for this exciting event, we would like to provide you with some additional details. <br><b>IN ORDER TO FINALLY CONFIRM YOUR REGISTRATION, YOU'LL RECEIVE A CALL AND ANOTHER EMAIL FROM US ABOUT CONFIRMING YOUR REGISTRATION.
    FAILING TO ADHERE WITH CONFIRMATION WILL INVALIDATE YOUR REGISTRATION, YOUR QRCODE, AND YOUR HEXCODE AUTOMATICALLY, AFTER WHICH YOU'LL HAVE TO REPEAT THE REGISTRATION PROCESS UNTIL REGISTRATIONS CLOSE.</b><br>
    <br>Some very important things you'll need now are:<br>
    <ul>
        <li style="font-family: Trebuchet MS;">Your Competition's Community Link: <a href="{codes[data["comp"]]}">{codes[data["comp"]]}</a></li>
        <li style="font-family: Trebuchet MS;">Your HEXCODE: <span style="font-weight:700; letter-spacing: 0.5rem;font-size: 18px;">{hex_code[:4]}</span></li>
        <li style="font-family: Trebuchet MS;">Your QRCODE attached at the end of this email</li>
    </ul>
    <br>For the provided attached Hexcode and QRcode, you will need to present them both to gain entry into the competition area.<br>
    <br>In due course, you will receive another email containing the rules and guidelines of the competition you have registered for, as well as general event protocols that you will need to follow on the event day.<br>
    <br>Please note that the leader of your team will be required to check in at the DEVDAY's DESK and collect the cards for their team. On the day of the event, no registration-related issues or requests such as expanding your team or adding a member will be addressed. We kindly request that you adhere to this process and contact us before the event day to ensure a smooth and successful event.<br>
    <br>We cannot wait to welcome you to SYSTEMS LIMITED DEVDAY 2023, and we assure you that our team will leave no stone unturned to ensure that you have an unforgettable experience.<br>
    <br>Mark the date, 4TH MAY 2023 (Thursday), in your calendar, and get ready for an eventful DEVDAY this year!<br>
    <br>Thank you once again for your participation, and we are eagerly looking forward to seeing you on the event day!<br>
    <br>Best Regards,<br>
    <br>Team SYSTEMS LIMITED DEVDAY 2023,<br>ACM-NUCES Karachi.
    <br>Contact us: <a mailto="admin@devday23.tech">admin@devday23.tech</a></body>'''

    msg.attach(MIMEText(message, 'html'))

    file_location = f"qrcodes/{data['email']}.png"
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, data['email'], text)
    server.quit()
    return

def qrgen(data):
    data["email"]=data["email"].lower()
    data = dict(sorted(data.items()))
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
    if "key" not in data.keys():
        data['key'] = 11798

    togo = {"Name":data['name'], "Email":data['email'].lower(), "Contact":data['contact'], "Hexcode":str(hashfunc(data['email'])[:5]), "key":data['key']}
    togo = dict(sorted(togo.items()))
    for all in togo.keys():
        togo[all] = str(togo[all]) + "\\" # \\ is used to separate the fields within the QR

    qr.add_data(togo)
    qr.make()

    img = qr.make_image(fill_color="white", back_color="teal")
    print(os.getcwd())
    img.save(f"qrcodes/{data['email'].lower()}.png")
    for all in togo.keys():
        togo[all] = togo[all][:-1]

    mailer(data)
    return

def mail_message(message, data):
    msg = MIMEMultipart()
    msg['From'] = "Fouzan Asif"
    msg['To'] = data['email']
    msg['Subject'] = f"OTP for Registration - {data['name']}"

    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, data['email'], text)
    server.quit()

def mark_yellow(wks,row):
    c1 = "A" + str(row)
    c2 = "F" + str(row)
    wks.format(c1 + ":" + c2, {'backgroundColor': {'red': 1.0 , 'green' : 1.0 , 'blue' : 0.0}})

def mark_green(wks,row):
    c1 = "A" + str(row)
    c2 = "F" + str(row)
    wks.format(c1 + ":" + c2, {'backgroundColor': {'red': 0.0 , 'green' : 1.0 , 'blue' : 0.0}})


