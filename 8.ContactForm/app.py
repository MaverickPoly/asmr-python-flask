# Email sender app, send email to specific users when submitting a form
from flask import Flask, request, render_template, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
SMTP_SERVER = "smtp.gmail.com"
SMTP_POST = 587

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        sender_email = request.form.get("sender_email")
        receiver_email = request.form.get("receiver_email")
        password = request.form.get("password")
        subject = request.form.get("subject")
        body = request.form.get("body")
        send_email(sender_email, receiver_email, password, subject, body)
    return render_template("index.html")


def send_email(sender_email, receiver_email, password, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_POST) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message, sender_email, receiver_email)
            flash("Email send successfully")
    except Exception as e:
        flash(f"Error sending email: {e}")



if __name__ == "__main__":
    app.run(debug=True)
