from flask import Flask
from flask_mail import Mail,Message
import os
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('hongnguye617@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('selvcnvaqaduogji')
app.config['MAIL_DEFAULT_SENDER'] = 'hongnguye617@gmail.com'
mail = Mail(app)
users=['nghiemthithoa10@gmail.com','nghiemthoa697@gmail.com']
@app.route("/")
def index():
    with mail.connect() as conn:
        for user in users:
            message = 'ngayffffffffffffffffffffff'
            subject = "hello, %s" % user
            msg = Message(recipients=[user],
                          body=message,
                          subject=subject)

            conn.send(msg)
if __name__ == '__main__':
    app.run(debug=True)