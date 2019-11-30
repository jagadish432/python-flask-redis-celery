from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from celery import Celery
from db.db import *
from db.models import *
from utils.common import *
app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

# set up Flask-Mail Integration
mail = Mail(app)


# setup celery client
client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# client.conf.update(app.config)


# Add this decorator to our send_mail function
@client.task
def send_mail(data):
    """ Function to send emails.
    """
    with app.app_context():
        msg = Message("Ping!",
                    sender="maheshbabu4329@gmail.com",
                    recipients=[data['email']])
        msg.body = data['message']
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        email = request.form['email']
        user = User(email)
        user.name = request.form['name']
        user.password = get_hash(request.form['password'])
        status, record = get_record('''select name, email from users where email=?''', user)
        print("status is ", status)
        if status is False:
            create_status = create_user_record(''' INSERT INTO users(name, phone, email, password)
                  VALUES(:name, :phone, :email, :password)''', user)
            print(create_status)
            if create_status:
                flash("User created Successfully.", "info")
            else:
                flash("User creation failed, please try again !!", "danger")
        else:
            flash("A user (" + record[0] + ") with this email id already exists !!", "danger")

        return redirect(url_for('index'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        user = User(request.form['email'])
        user.password = get_hash(request.form['password'])
        user_exists, record = get_record('''select email, password from users where email=?''', user)
        if not user_exists:
            flash("User doesn't exist with this email id", "danger")
        else:
            if record[1] == user.password:
                flash("User logged in successfully.", "info")
            else:
                flash("Wrong password, please try again.", "danger")
                return redirect(url_for('index'))
    return redirect(url_for('notify'))

@app.route('/notify', methods=['GET','POST'])
def notify():
    if request.method == "GET":
        return render_template('notify.html')
    elif request.method == "POST":
        user = User(request.form['email'])
        user_exists, record = get_record('''select email, password, id from users where email=?''', user)
        if not user_exists:
            flash("User doesn't exist with this email id", "danger")
        user.id = record[2]
        notify = Notify(request.form['message'], user)
        notify.user_id = record[2]
        duration = int(request.form['duration'])
        duration_unit = request.form['duration_unit']

        duration_units = {
            "1" : "minutes",
            "2": "hours",
            "3": "days"
        }
        duration_unit = duration_units[duration_unit]
        print("duration unit is - ", duration_unit)

        if duration_unit == 'minutes':
            duration *= 60
        elif duration_unit == 'hours':
            duration *= 3600
        elif duration_unit == 'days':
            duration *= 86400


        notify.duration = duration
        status, record = create_notification_record('''
                        insert into notifications(name, email, created_at, scheduled_at, userId, status) 
                        VALUES(:name, :email, :created_at, :scheduled_at, :userId, :status)''',
                        notify, user)
        if not status:
            flash("Unable to create notification scheduler, please try again!!", "danger")
        else:
            flash("Successfully created notification scheduler", "info")

            send_mail.apply_async(args=[{"email": user.email, "message": notify.message}], countdown=notify.duration)
            # send_mail(data={"email": user.email, "message": notify.message})
            flash(f"Email will be sent to {user.email} in {request.form['duration']} {duration_unit}")

        return redirect(url_for('notify'))

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        return render_template('notify.html')

if __name__ == '__main__':
    app.run(debug=True)