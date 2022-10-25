from flask import Flask, render_template, url_for, request, redirect
import csv
import requests
application = Flask(__name__)

@application.route('/')
def my_home():
    return render_template('index.html')

@application.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject, message])

def send_msg(text):
   token = "5742127079:AAEExSw-Ox8RGbhoQqO3-NbT3nwnNj4nKHY"
   chat_id = "678344870"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
   results = requests.get(url_req)
   print(results.json())

def telegram_bot_send_document():
    bot_token = "5742127079:AAEExSw-Ox8RGbhoQqO3-NbT3nwnNj4nKHY"
    bot_chatId = "678344870"

    a = open('database.txt', 'rb')
    send_document = 'https://api.telegram.org/bot' + bot_token +'/sendDocument?'
    data = {
    'chat_id': bot_chatId,
    'parse_mode':'HTML',
    'caption':'This is my file'
    }

    r = requests.post(send_document, data=data, files={'document': a},stream=True)
    print(r.url)

    return r.json()


@application.route('/submit_form', methods = ['POST','GET'])
def submit_form():
    if request.method=='POST':
        data=request.form.to_dict()
        write_to_csv(data)

        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        data2 = email+"\n"+subject+"\n\n"+message
        send_msg(data2)
        telegram_bot_send_document()

        return redirect("/thankyou.html")
    else:
        return "Something Went Wrong..."

