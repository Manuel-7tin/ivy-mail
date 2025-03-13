from flask import Flask, abort, render_template, redirect, url_for, flash, request
import pandas as pd
import datetime as dt
import ssl
import smtplib
from email.message import EmailMessage
from io import StringIO
import threading
import os
import re
import base64
from email.utils import make_msgid
import socket
import  time

app = Flask(__name__)


def save_base64_image(data, num):
    # Extract base64 data from the src attribute
    img_data = re.search(r'base64,(.*)', data).group(1)
    img_bytes = base64.b64decode(img_data)

    # Save as image file
    image_filename = f'uploaded_image{num}.png'
    with open(image_filename, 'wb') as f:
        f.write(img_bytes)
    return image_filename

def handle_image(letter):
    image_cid = []
    images = []

    # Extract base64 images and replace with file URLs or attachments
    img_tags = re.findall(r'<img src="data:image/[^;]+;base64,[^"]+"', letter)
    # Create a unique image cid for each image
    for i in range(len(img_tags)):
        image_cid.append(make_msgid(domain="example.com"))

    # Process each image
    for index, img_tag in enumerate(img_tags):
        img_src = re.search(r'src="([^"]+)"', img_tag).group(1)

        # Save the image file
        uploaded_image = save_base64_image(img_src, index)
        images.append((uploaded_image, "jpg"))
        letter = letter.replace(img_src, f"cid:{image_cid[index]}")
    return letter, images, image_cid


def attach_image(images, msg, image_cid):
    for idx, imgtup in enumerate(images):
        imgfile, imgtype = imgtup
        with open(imgfile, "rb") as img:
            msg.add_related(
                img.read(),
                maintype="image",
                subtype="jpg",
                cid=f"<{image_cid[idx]}>")

def send_email(data, msg):
    # print(msg, data)
    mail_sender = "ivyleagueupdates@gmail.com"
    PASSWORD = "lxdmjkyryqwqxbml"
    # mail_sender = os.getenv("MAIL_ADDR")
    # PASSWORD = os.getenv("PWORD")
    msg_subject = msg[0]
    msg_body = msg[1]

    # Set and replace placeholder date in content.
    date = dt.datetime.now()
    f_date = date.strftime("%H:%M | %b %d, %Y.")
    new_letter = msg_body.replace("[Date]", f_date)
    new_letter, images, image_cid = handle_image(new_letter)

    # Send mail per recipient
    for person in data:
        print(person["name"])
        # 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
        personalized_letter = new_letter.replace("[Name]", person["name"])
        # with open("review.txt", mode="w") as txt_file:
        #     txt_file.write(personalized_letter)
        with open("image.html", mode="w") as html_file:
            html_file.write(personalized_letter)

        # 4. Send the letter generated in step 3 to that person's email address.
        message = EmailMessage()
        message["From"] = f"Ivy League Updates <{mail_sender}>"
        message["To"] = person["email"]
        message["Subject"] = msg_subject
        attach_image(images, message, image_cid)
        # message.set_content(personalized_letter)
        message.add_alternative(personalized_letter, subtype='html')
        message.add_header("Reply-to", "updates@ivyleaguenigeria.com")

        context = ssl.create_default_context()
        breaks = 0
        while True:
            try:
                with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=context) as mail:
                    mail.login(user=mail_sender, password=PASSWORD)
                    mail.sendmail(from_addr=mail_sender, to_addrs=person["email"], msg=message.as_string())
            except smtplib.SMTPConnectError as f:
                print("error as", f)
            except smtplib.SMTPException as e:
                print("Encountered smtp error :", e)
                break
            except socket.gaierror as e:
                print("there is an error:", e)
                breaks += 1
                time.sleep(3)
                if breaks > 4:
                    # error404()
                    break
            else:
                break


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
    if request.method == "POST":
        # Get the uploaded CSV file
        csv_file = request.files['csvFile']
        if csv_file:
            # Process the file as needed
            pass

        # Get the message content as HTML
        message_html = request.form.get('message')
        if message_html:
            print("Message as HTML:", message_html)
            # You can store this HTML, render it, or process it further

        # Redirect immediately
        return redirect("https://www.twitter.com")
    return render_template("temp2.html")


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
