from flask_mail import Mail

app.config["MAIL_SERVER"] = "stmp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "riselucky30@gmail.com"
app.config["MAIL_PASSWORD"] = "mvgw itrm guqi koix"
app.config["MAIL_DEFAULT_SENDER"]= "riselucky30@gmail.com"

mail = Mail(app)
