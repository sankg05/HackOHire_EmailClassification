from flask import jsonify, request
from emailclassifier import app
import requests
import joblib
import os
import socket
import numpy as np
import time
from itertools import chain
import email
import imaplib
from email.header import decode_header
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import xgboost
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib


spam_model = joblib.load('emailclassifier/email_classifier_model.pkl')
API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
imap_host = 'imap.gmail.com'
imap_port = 993
username = 'sanikagadkari05@gmail.com'
cls_model = joblib.load('emailclassifier/xg_model.pkl')
count_vectorizer = joblib.load('emailclassifier/cv1.pkl')

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def has_html_tags(text):
    pattern = re.compile(r'<[^>]+>')
    return bool(pattern.search(text))

def RemoveHTMLTags(strr):
    # Print string after removing tags
    return re.compile(r'<[^>]+>').sub('', strr)

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))

def text_cleaner(text):
    corpus = []
    review = re.sub('[^a-zA-Z]', ' ', text)  # Remove non-alphabetic characters
    review = review.lower()  # Convert to lowercase
    review = review.split()  # Split into words
    ps = PorterStemmer()  # Create stemmer
    all_stopwords = stopwords.words('english')  # Get English stopwords
    all_stopwords.remove('not')  # Remove 'not' from stopwords
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]  # Stem and remove stopwords
    review = ' '.join(review)  # Join words back into a string
    corpus.append(review)
    return corpus  # Return as a list containing a single element

def message(subject, text):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    return msg

def email_router(subject, text, class_index):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('sanikagadkari05@gmail.com', os.getenv('SMTP_PASSWORD'))
    msg = message(subject, text)

    if class_index == 0:
        to = ["mohit.agarwal@spit.ac.in"]
        smtp.sendmail(from_addr=username, to_addrs=to, msg=msg.as_string())
    elif class_index == 1:
        to = ["ankitdighe2014@spit.ac.in"]
        smtp.sendmail(from_addr=username, to_addrs=to, msg=msg.as_string())
    elif class_index == 2:
        to = ["sanika.gadkari@spit.ac.in"]
        smtp.sendmail(from_addr=username, to_addrs=to, msg=msg.as_string())
    elif class_index == 3:
        to = ["ankit.dighe@spit.ac.in"]
        smtp.sendmail(from_addr=username, to_addrs=to, msg=msg.as_string())
    else:
        to = ["deepali.daga@spit.ac.in"]
        smtp.sendmail(from_addr=username, to_addrs=to, msg=msg.as_string())
    smtp.quit()

@app.route('/', methods = ['GET', 'POST'])
def hello():
    return f'Hello! Container ID: {socket.gethostname}'

@app.route('/urgency', methods = ['GET', 'POST'])
def urgency():
    body = "Critical system outage affecting production servers, action needed immediately"
    # data = request.get_json()
    # body = data.get('body')
    payload = {
        "inputs": body,
        "parameters": {"candidate_labels": ["urgent", "not urgent"]},
    }
    headers = {"Authorization": f"Bearer {os.getenv('API_TOKEN')}"}
    response = requests.post(API_URL, headers=headers, json = payload)
    pred_label_id = np.argmax(response.json()['scores'])
    pred_label = response.json()['labels'][pred_label_id]
    #return jsonify({"urgency_pred": pred_label})
    print(pred_label)

#For Real time classification model
@app.route('/realtime_classify', methods = ['GET', 'POST'])
def realtime_classify():
    criteria = {}
    uid_max = 0
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(username, os.getenv('SMTP_PASSWORD'))
    #select the folder
    mail.select('inbox')
    result, data = mail.uid('SEARCH', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]
    if uids:
        uid_max = max(uids)
    mail.logout()

    id = ''
    body = ''
    while 1:
        mail = imaplib.IMAP4_SSL(imap_host)
        mail.login(username, os.getenv('SMTP_PASSWORD'))
        mail.select('inbox')
        result, data = mail.uid('search', None, search_string(uid_max, criteria))
        uids = [int(s) for s in data[0].split()]

        for uid in uids:
            # Have to check again because Gmail sometimes does not obey UID criterion.
            if uid > uid_max:
                result, msg = mail.uid('fetch', str(uid), '(RFC822)')
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        id, encoding = decode_header(msg["Message-ID"])[0]
                        if msg.is_multipart():
                        # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                    if has_html_tags(body):
                                        body = RemoveHTMLTags(body)
                                except:
                                    pass
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode()
                        vec = text_cleaner(body)
                        class_index = cls_model.predict(count_vectorizer.transform(vec))
                        email_router(subject, body, class_index)
                uid_max = uid
    mail.logout()
    time.sleep(1)

@app.route('/batch_classify', methods = ['GET', 'POST'])
def batch_classify():
    imap = imaplib.IMAP4_SSL(imap_host)
    imap.login(username, os.getenv('SMTP_PASSWORD'))
    status, messages = imap.select("Inbox")
    # number of top emails to fetch
    N = 1
    # total number of emails
    messages = int(messages[0])
    id = ''
    body = ''
    label = 'Finance'
    tmp, msg = imap.search(None, 'ALL')
    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                id, encoding = decode_header(msg["Message-ID"])[0]
                if msg.is_multipart():
                # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                            if has_html_tags(body):
                                body = RemoveHTMLTags(body)
                        except:
                            pass
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
        vec = text_cleaner(body)
        class_index = cls_model.predict(count_vectorizer.transform(vec))
        email_router(subject, body, class_index)
    # close the connection and logout
    imap.close()


