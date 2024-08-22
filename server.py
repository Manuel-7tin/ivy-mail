from flask import Flask, abort, render_template, redirect, url_for, flash, request
import pandas as pd
import datetime as dt
import ssl
import smtplib
from email.message import EmailMessage
from io import StringIO
import threading
import os

app = Flask(__name__)

def send_email(data, msg):
    print(msg, data)
    mail_sender = os. getenv("MAIL")
    PASSWORD = os. getenv("PWORD")
    date = dt.datetime.now()
    f_date = date.strftime("%H:%M | %b %d, %Y.")
    msg_subject = msg[0]
    msg_body = msg[1]
    new_letter = msg_body.replace("[Date]", f_date)

    for person in data:
        print(person["name"])
        # 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
        personalized_letter = new_letter.replace("[Recipient's_First_Name]", person["name"])

        # 4. Send the letter generated in step 3 to that person's email address.
        message = EmailMessage()
        message["From"] = mail_sender
        message["To"] = person["email"]
        message["Subject"] = msg_subject
        # message.set_content(personalized_letter)
        message.add_alternative(personalized_letter) #, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as mail:
            mail.login(user=mail_sender, password=PASSWORD)
            mail.sendmail(from_addr=mail_sender, to_addrs=person["email"], msg=message.as_string())


@app.route("/")
def page():
    print("in again")
    print(request.method)
    return render_template("index.html")

@app.route("/mail", methods=["GET", "POST"])
def send_msg():
    if request.method == "POST":
        uploaded_file = request.files.get("csvFile")        # Get the filename
        file_name = uploaded_file.filename
        print(f"Uploaded file name: {file_name}, {type(file_name)}")
        file_type = file_name.split('.')[1]
        if file_type == "csv":
            data = pd.read_csv(StringIO(uploaded_file.stream.read().decode('utf-8')))
        elif file_type == "xlsx" or file_type == "xls":
            data = pd.read_excel(StringIO(uploaded_file.stream.read().decode('utf-8')))
        else:
            data = None

        # print(f"Tiop, {type(data)}")
        # print(data is not None)
        if data is not None:
            data.fillna("Dear Customer", inplace=True)
            data_dicts = data.to_dict(orient="records")
            message = request.form
            mail_subject = message.get("subject")
            mail_body = message.get("body")
            email_thread = threading.Thread(target=lambda: send_email(data_dicts, [mail_subject, mail_body]))
            email_thread.start()
    return redirect(url_for("page"))


@app.route("/sms", methods=["GET", "POST"])
def send_text():
    print("omolomo")


@app.route("/csv", methods=["GET", "POST"])
def take_csv():
    print("shashasahs")
    if request.method == "POST":
        print(type(request.form.get("csvFile")))
    # return redirect("www.google.com")

@app.route("/test", methods=["GET", "POST"])
def temp():
    print("habibi")
    print("file:", request.files.keys())
    print(request.form.keys())
    print(request.form.get("joko"))
    print(request.form.get("ekolo"))
    return render_template("temp.html")


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == "POST":
        # Get the uploaded CSV file
        print("filo", request.files.keys())
        csv_file = request.files['csvFile']
        if csv_file:
            # Read the CSV with pandas
            csv_data = pd.read_csv(StringIO(csv_file.stream.read().decode('utf-8')))
            # csv_data = pd.read_csv(csv_file)
            print("CSV Columns:", csv_data.columns.tolist())

        # Get the message
        message = request.form.get('message')
        if message:
            print("Message (First 10 characters):", message[:10])

        # Redirect to Google.com
        return redirect("https://www.google.com")
    return render_template("temp.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
