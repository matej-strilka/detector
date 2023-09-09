import smtplib, ssl, os

def send_mail(message):
    host = "smtp.gmail.com"
    port = 465
    username = "matejstrilka@gmail.com"
    username1 = "matejstrilka@seznam.cz"
    password = os.getenv("HESLO")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, username1, message)