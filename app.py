from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def send_email(subject, body):
    try:
       
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("padaliyabhavya834@gmail.com", "oybr xpyq tzfc uddk") 

       
        msg = MIMEMultipart()
        msg['From'] = "padaliyabhavya834@gmail.com"
        msg['To'] = "bhvyap67@gmail.com"
        msg['Subject'] = subject

        # Attach the body
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

    if send_email("Message from Portfolio Visitor", f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"):
        flash("Your message has been sent successfully!", "success")
    else:
        flash("There was an issue sending your message. Please try again.", "error")

    return redirect(url_for("home"))

@app.route("/hireme", methods=["POST"])
def hireme():
    client_name = request.form.get("client-name").strip()
    client_email = request.form.get("client-email").strip()
    project_title = request.form.get("project-title").strip()
    project_description = request.form.get("project-description").strip()
    service_type = request.form.get("service-type").strip()
    deadline = request.form.get("deadline").strip()
    budget = request.form.get("budget").strip()
    additional_notes = request.form.get("additional-notes").strip()

    subject = "New Project Inquiry from Hire Me Form"
    body = (f"Client Name: {client_name}\n"
            f"Client Email: {client_email}\n"
            f"Project Title: {project_title}\n"
            f"Project Description:\n{project_description}\n"
            f"Service Type: {service_type}\n"
            f"Deadline: {deadline}\n"
            f"Budget: {budget}\n"
            f"Additional Notes:\n{additional_notes}")

    if send_email(subject, body):
        flash("Your project inquiry has been sent successfully!", "success")
    else:
        flash("There was an issue sending your inquiry. Please try again.", "error")

    return redirect(url_for("home"))

@app.route("/hireme")
def hireme_form():
    return render_template("hireme.html")

if __name__ == "__main__":
    app.run(debug=True)
