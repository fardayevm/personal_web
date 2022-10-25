from flask import Flask, render_template, url_for, request, redirect
import csv

application = Flask(__name__)

@application.route('/')
def my_home():
    return render_template('index.html')

@application.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open('database.csv', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject, message])


@application.route('/submit_form', methods = ['POST','GET'])
def submit_form():
    if request.method=='POST':
        data=request.form.to_dict()
        write_to_csv(data)
        return redirect("/thankyou.html")
    else:
        return "Something Went Wrong..."
