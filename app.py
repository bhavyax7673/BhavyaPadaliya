from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

def send_email(name, email, message):
    try:
        # Set up the server
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("padaliyabhavya834@gmail.com", "oybr xpyq tzfc uddk")  # Replace with your password

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = "padaliyabhavya834@gmail.com"
        msg['To'] = "bhvyap67@gmail.com"
        msg['Subject'] = "Message from Portfolio Visitor"

        # Create the body of the email
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        s.send_message(msg)
        s.quit()

        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["POST"])
def contact():
    email = request.form.get("email").strip()
    name = request.form.get("name").strip()
    message = request.form.get("message").strip()

    if send_email(name, email, message):
        flash("Your message has been sent successfully!", "success")
    else:
        flash("There was an issue sending your message. Please try again.", "error")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
