
from django.shortcuts import render, redirect
from . import forms
from .models import Details
from .models import Compose
import imaplib,email
from gtts import gTTS
import os
from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import JsonResponse
import re
from django.core.mail import send_mail

file = "good"
i="0"
passwrd = ""
addr = ""
item =""
subject = ""
body = ""
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)
attachment_dir = 'C:/Users/SACHIN/OneDrive/Desktop/'


def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return

def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that. Could you please rephrase?")
        response = 'N'
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        response = 'N'
    except Exception as e:  # Catch generic exceptions for unexpected errors
        print("An unexpected error occurred: {0}".format(e))
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
    return temp

def read_mails(mail_list,folder):
    global s, i
    mail_list.reverse()
    mail_count = 0
    to_read_list = list()
    for item in mail_list:
        result, email_data = conn.fetch(item, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        texttospeech("Email number " + str(mail_count + 1) + "    .The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject, file + i)
        i = i + str(1)
        print('message id= ', Msg_id)
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        print("\n")
        to_read_list.append(Msg_id)
        mail_count = mail_count + 1

def search_specific_mail(folder,key,value,foldername):
    global i, conn
    conn.select(folder)
    result, data = conn.search(None,key,'"{}"'.format(value))
    mail_list=data[0].split()
    if len(mail_list) != 0:
        texttospeech("There are " + str(len(mail_list)) + " emails with this email ID.", file + i)
        i = i + str(1)
    if len(mail_list) == 0:
        texttospeech("There are no emails with this email ID.", file + i)
        i = i + str(1)
    else:
        read_mails(mail_list,foldername)

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def login_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        passwrd = 'hiep aodb itic nltd'
        addr = 'majorprojectit2024@gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, passwrd)
            s.login(addr, passwrd)
            texttospeech("I have logged you in successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})

    
    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'homepage/login.html', {'detail' : detail}) 


def options_view(request):
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        texttospeech("You are logged into your account. What would you like to do ?", file + i)
        i = i + str(1)
        while(flag):
            texttospeech("Say compose to compose an email. Say inbox for Inbox folder.Say sent for Sent folder. Say trash for Trash folder.Say logout to Logout. Do you want me to repeat?", file + i)
            i = i + str(1)
            say = speechtotext(10)
            print(f"yes/no: {say}")
            if say == 'No' or say == 'no' or say=='noo' or say=='nyo':
                flag = False
        texttospeech("Enter your desired action", file + i)
        i = i + str(1)
        act = speechtotext(10)
        # act = act.lower()
        print(f"Chosen action: {act}")
        
        if act == 'compose' or act== 'kompos' or act=='kampos' or act == 'kampoj':
            return JsonResponse({'result' : 'compose'})
        elif act == 'inbox' :
            return JsonResponse({'result' : 'inbox'})
        elif act == 'sent' or act=='send'  or act == 'shoot':
            return JsonResponse({'result' : 'sent'})
        elif act == 'trash':
            return JsonResponse({'result' : 'trash'})
        elif act == 'logout' or act =='log out':
            addr = ""
            passwrd = ""
            texttospeech("You have been logged out of your account and now will be redirected back to the login page.",file + i)
            i = i + str(1)
            return JsonResponse({'result': 'logout'})
        else:
            texttospeech("Invalid action. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
    elif request.method == 'GET':
        return render(request, 'homepage/options.html')



def compose_view(request):
    global i, addr, passwrd, s, item, subject, body
    if request.method == 'POST':
        text1 = "You have reached the page where you can compose and send an email. "
        texttospeech(text1, file + i)
        i = i + str(1)
        flag = True
        flag1 = True
        fromaddr = 'majorprojectit2024@gmail.com'
        passwd = 'hiep aodb itic nltd'
        # toaddr = list()
        while flag1:
            while flag:
                texttospeech("enter receiver's email address:", file + i)
                i = i + str(1)
                toaddr = ""
                toaddr = speechtotext(15)
                print(f"receiver address: {toaddr}")
                if toaddr != 'N':
                    
                    texttospeech("You meant " + toaddr + " say yes or correct to confirm or no to enter again", file + i)
                    i = i + str(1)
                    say = speechtotext(5)
                    say = say.lower()
                    print(f"action: {say}")
                    if say == 'yes' or say == 'es' or say=='s' or say == 'correct':
                        # toaddr.append(to)
                        flag = False
                else:
                    texttospeech("could not understand what you meant", file + i)
                    i = i + str(1)
            # texttospeech("Do you want to enter more recipients ?  Say yes or no.", file + i)
            # i = i + str(1)
            say1 = 'No'
            if say1 == 'No' or say1 == 'no':
                flag1 = False
            flag = True

        
        toaddr = toaddr.strip()
        toaddr = toaddr.replace(' ', '')
        toaddr = toaddr.lower()
        toaddr = convert_special_char(toaddr)
        print(toaddr)


        msg = MIMEMultipart()
        msg['From'] = fromaddr
        print(f"From Address: {msg['From']}")
        msg['To'] = toaddr
        print(f"To Address: {msg['To']}")
        flag = True
        while (flag):
            texttospeech("enter subject", file + i)
            i = i + str(1)
            subject = speechtotext(10)
            print(f"Subject action: {subject}")
            if subject == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False
        msg['Subject'] = subject
        flag = True
        while flag:
            texttospeech("enter body of the mail", file + i)
            i = i + str(1)
            body = speechtotext(20)
            print(f"Body action: {body}")
            if body == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False

        msg.attach(MIMEText(body, 'plain'))
        texttospeech("If there are any attachments say the keyworrd attachment , else say no", file + i)
        i = i + str(1)
        x = speechtotext(3)
        x = x.lower()
        print(x)
        if x == 'attachment' or x=='attach':
            texttospeech("If you want to record an audio and send as an attachment say the keyword continue", file + i)
            i = i + str(1)
            say = speechtotext(2)
            say = say.lower()
            print(say)
            if say == 'continue' or say == 'continew':
                texttospeech("Enter filename.", file + i)
                i = i + str(1)
                print(filename)
                filename = filename.lower()
                filename = filename + '.mp3'
                filename = filename.replace(' ', '')
                print(filename)
                texttospeech("Speak your audio message.", file + i)
                i = i + str(1)
                audio_msg = speechtotext(10)
                flagconf = True
                while flagconf:
                    try:
                        tts = gTTS(text=audio_msg, lang='en', slow=False)
                        tts.save(filename)
                        flagconf = False
                    except:
                        print('Trying again')
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
            elif say == 'no' or say == 'n':
                texttospeech("Enter filename with extension", file + i)
                i = i + str(1)
                filename = speechtotext(5)
                filename = filename.strip()
                filename = filename.replace(' ', '')
                filename = filename.lower()
                filename = convert_special_char(filename)
                
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Start TLS encryption

    # Authenticate with username and password
            server.login(fromaddr, passwd)
            s.sendmail(fromaddr, toaddr, msg.as_string())
            texttospeech("Your email has been sent successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
        except smtplib.SMTPHeloError as e:
            print("Error: The server didn't respond properly to the greeting. Please check your server configuration.")
            texttospeech("Sorry, your email failed to send. There may be a problem with the mail server. You will now be redirected to the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        except smtplib.SMTPRecipientsRefused as e:
            print("Error: The server rejected ALL recipients. Check recipient addresses.")
            texttospeech("Sorry, your email failed to send. The recipient addresses may be invalid. You will now be redirected to the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        except smtplib.SMTPSenderRefused as e:
            print("Error: The server didn't accept the from address. Check your sender email settings.")
            texttospeech("Sorry, your email failed to send. There may be a problem with your sender email address. You will now be redirected to the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        except smtplib.SMTPDataError as e:
            print("Error: The server responded with an unexpected error. Check server logs for details.")
            texttospeech("Sorry, your email failed to send. There may be a temporary issue with the mail server. You will now be redirected         to the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        except smtplib.SMTPNotSupportedError as e:
            print("Error: The server doesn't support the requested mail option (e.g., SMTPUTF8).")
            texttospeech("Sorry, your email failed to send. There may be a configuration issue with the mail server. You will now be        redirected to the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        except Exception as e:  # Catch generic exceptions for unexpected errors
            print("An unexpected error occurred:", e)
            texttospeech("Sorry, your email failed to send. An unexpected error occurred. You will now be redirected to the compose page        again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})

        
        s.quit()
        return JsonResponse({'result' : 'success'})
    
    compose  = Compose()
    compose.recipient = item
    compose.subject = subject
    compose.body = body

    return render(request, 'homepage/compose.html', {'compose' : compose})


def inbox_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        addr = 'majorprojectit2024@gmail.com'
        passwd = 'hiep aodb itic nltd'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, passwrd)
        conn.select('"INBOX"')
        result, data = conn.search(None, '(UNSEEN)')
        unread_list = data[0].split()
        no = len(unread_list)
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your inbox. There are " + str(len(mail_list)) + " total mails in your inbox. You have " + str(no) + " unread emails" + ". To read unread emails say unread. To search a specific email say search. To go back to the menu page say back. To logout say logout."
        texttospeech(text, file + i)
        i = i + str(1)
        flag = True
        while(flag):
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == 'unread':
                flag = False
                if no!=0:
                    read_mails(unread_list,'inbox')
                else:
                    texttospeech("You have no unread emails.", file + i)
                    i = i + str(1)
            elif act == 'search':
                flag = False
                emailid = ""
                while True:
                    texttospeech("Enter email ID of the person who's email you want to search.", file + i)
                    i = i + str(1)
                    emailid = speechtotext(15)
                    print(emailid)
                    texttospeech("You meant " + emailid + " say correct to confirm or no to enter again", file + i)
                    i = i + str(1)
                    yn = speechtotext(5)
                    yn = yn.lower()
                    print(yn)
                    if yn == 'correct':
                        break
                emailid = emailid.strip()
                emailid = emailid.replace(' ', '')
                emailid = emailid.lower()
                emailid = convert_special_char(emailid)
                search_specific_mail('INBOX', 'FROM', emailid,'inbox')

            elif act == 'back':
                texttospeech("You will now be redirected to the menu page.", file + i)
                i = i + str(1)
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'log out' or act == 'logout':
                addr = ""
                passwrd = ""
                texttospeech("You have been logged out of your account and now will be redirected back to the login page.", file + i)
                i = i + str(1)
                return JsonResponse({'result': 'logout'})

            else:
                texttospeech("Invalid action. Please try again.", file + i)
                i = i + str(1)

        texttospeech("You will now be redirected to the menu page.", file + i)
        i = i + str(1)
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'homepage/inbox.html')
    
   