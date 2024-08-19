from flask import Flask, abort, render_template, redirect, url_for, flash, request

app = Flask(__name__)

@app.route("/")
def page():
    print("in again")
    print(request.method)
    return render_template("index.html")

@app.route("/mail", methods=["GET", "POST"])
def send_msg():
    print("omo")
    print(request.method)
    if request.method == "POST":
        print("in")
        data = request.form
        mail_subject = data.get("subject")
        print(f"ss{mail_subject}ll")
        mail_body = data.get("message_body")
        print(f"ww{mail_body}ll")
    return redirect(url_for("page"))


@app.route("/sms", methods=["GET", "POST"])
def send_text():
    print("omolomo")


@app.route("/csv", methods=["GET", "POST"])
def take_csv():
    print("shashasahs")
    if request.method == "POST":
        print(type(request.form.get("csv")))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
