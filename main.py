from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import sys
import os

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'hyukzuny@gmail.com',
	MAIL_PASSWORD = '#'
	)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/work/<project>')
def work(project):
	if (project == 'cognitive-services'):
		return render_template('cognitive-services.html')
	elif (project == 'image-processing'):
		return render_template('image-processing.html')
	elif (project == 'object-detection'):
		return render_template('object-detection.html')
	elif (project == 'raspberry-pi-lab'):
		return render_template('raspberry-pi-lab.html')
	elif (project == 'deep-learning-for-advanced-driver-assistance-system-applications'):
		return render_template('deep-learning-for-advanced-driver-assistance-system-applications.html')


@app.route('/email', methods=['POST', 'GET'])
def send_email_button():
	if request.method == 'POST':
		first_name = request.form['fname']
		last_name = request.form['lname']
		sender_email = request.form['sender']
		subject = request.form['subject']
		message_content = request.form['message']


		result = send_email(first_name, last_name, sender_email, subject, message_content)
		

		if not result:
			return redirect('/')
		else:
			return render_template('index.html', content="FAILED TO SEND EMAIL")
	else:
		return render_template('index.html',)


def send_email(first_name, last_name, sender_email, in_subject, message_content):
	try:
		mail = Mail(app)
		msg = Message(subject=in_subject, sender=sender_email, recipients=["computer@khu.ac.kr"])
		#msg = Message(subject='test', sender="hyukzuny@gmail.com", recipients=["computer@khu.ac.kr"])
		msg.body = 'fname:\t\t' + first_name + '\n' + 'lname:\t\t' + last_name + '\n' + 'sender:\t\t' + sender_email + '\n' + 'content:\t' + message_content
		mail.send(msg)
	except Exception:
		print('email system error:')
		pass
	finally:
		pass




if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80, debug = True)