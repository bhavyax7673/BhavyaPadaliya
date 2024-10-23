from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Portfolio.db"
db = SQLAlchemy(app)

class ClientProjects(db.Model):

    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    client_name = db.Column(db.String)
    client_email = db.Column(db.String)
    project_title = db.Column(db.String)
    project_description = db.Column(db.Text)
    service_type = db.Column(db.String)
    deadline = db.Column(db.String)
    budget = db.Column(db.Integer)
    additional_notes = db.Column(db.String)

    def __init__(self,client_name,client_email,project_title,project_desc,service_type,deadline,budget,additional_notes):
        self.client_name = client_name
        self.client_email = client_email
        self.project_title = project_title
        self.project_description = project_desc
        self.service_type = service_type
        self.deadline = deadline
        self.budget = budget
        self.additional_notes = additional_notes

def send_email(to,subject, body):
    try:
       
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("padaliyabhavya834@gmail.com", "oybr xpyq tzfc uddk") 

       
        msg = MIMEMultipart()
        msg['From'] = "padaliyabhavya834@gmail.com"
        msg['To'] = to
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

@app.route("/contact", methods=["POST"])
def contact():
    email = request.form.get("email").strip()
    name = request.form.get("name").strip()
    message = request.form.get("message").strip()

    if send_email("bhvyap67@gmail.com","Message from Portfolio Visitor", f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"):

        flash("Your message has been sent successfully!", "success")

        
    else:
        flash("There was an issue sending your message. Please try again.", "error")

    return redirect(url_for("home"))

@app.route("/test")
def test():
    
    client = ClientProjects.query.first()

    return client.client_name

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
    body = (f"Dear [Your Name],\n\n"
            f"You have received a new project inquiry from your portfolio site. Below are the details:\n\n"
            f"**Client Name:** {client_name}\n"
            f"**Client Email:** {client_email}\n"
            f"**Project Title:** {project_title}\n"
            f"**Project Description:**\n{project_description}\n"
            f"**Service Type:** {service_type}\n"
            f"**Deadline:** {deadline}\n"
            f"**Budget:** {budget}\n"
            f"**Additional Notes:**\n{additional_notes}\n\n"
            f"Please review the details and get back to the client as soon as possible.\n\n"
            f"Best regards,\n")

    # Send email to the developer
    if send_email("bhvyap67@gmail.com", subject, body):
        flash("Your project inquiry has been sent successfully!", "success")
        client = ClientProjects(client_name=client_name,client_email=client_email,project_title=project_title,project_desc=project_description,service_type=service_type,deadline=deadline,budget=budget,additional_notes=additional_notes)
        db.session.add(client)
        db.session.commit()

       
        confirmation_subject = "Confirmation of Your Project Inquiry"
        confirmation_body = (f"Dear {client_name},\n\n"
                             f"Thank you for reaching out to me regarding your project titled \"{project_title}\". I have successfully received your inquiry and appreciate the information you provided.\n\n"
                             f"Here are the details you submitted:\n\n"
                             f"**Project Title:** {project_title}\n"
                             f"**Project Description:**\n{project_description}\n"
                             f"**Service Type:** {service_type}\n"
                             f"**Deadline:** {deadline}\n"
                             f"**Budget:** {budget}\n"
                             f"**Additional Notes:**\n{additional_notes}\n\n"
                             f"I value the opportunity to potentially work with you on this project. However, I would like to review your requirements in more detail during our discussion to ensure I can meet your expectations and provide the best possible service.\n\n"
                             f"I will send you a meeting link along with available times for us to discuss further. If the suggested time does not work for you, please feel free to reply to this email with your preferred timing.\n\n"
                             f"Thank you once again for considering me for your project. I look forward to our conversation and exploring how I can assist you.\n\n"
                             f"Best regards,\n"
                             f"Bhavya Padaliya\n"
                             f"https://padaliya-bhavya.vercel.app/\n")

        send_email(client_email, confirmation_subject, confirmation_body)  # Send confirmation to client
    else:
        flash("There was an issue sending your inquiry. Please try again.", "error")

    return redirect(url_for("home"))


@app.route("/hireme")
def hireme_form():
    return render_template("hireme.html")

if __name__ == "__main__":
    app.run(debug=True)
