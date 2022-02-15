import os
import smtplib

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

SECRET_KEY = os.urandom(32)

# TODO Env Variables
WEB_EMAIL = "monk3yd.thelab@gmail.com"  # WebApp Email
WEB_PWD = "raftel12345"
MY_EMAIL = "monk3yd.thelab@yahoo.com"  # My Personal Email

class ContactForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()], render_kw={"placeholder": "Your Name"})
    email = EmailField(label="Email", validators=[DataRequired()], render_kw={"placeholder": "Your Email"})
    subject = StringField(label="Subject", validators=[DataRequired()], render_kw={"placeholder": "Subject"})
    message = StringField(label="Message", widget=TextArea(), validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField(label="Send Message")


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=WEB_EMAIL, password=WEB_PWD)
            connection.sendmail(
                from_addr=WEB_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject: {form.subject.data}\n\n{form.message.data}"
            )
    return render_template("index.html", form=form)


# @app.route("/portfolio-details")
# def portfolio():
#     return render_template("portfolio-details.html")

if __name__ == "__main__":
    app.run(debug=True)
