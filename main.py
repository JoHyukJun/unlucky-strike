from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message

from werkzeug import secure_filename



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
	MAIL_PASSWORD = '#',

	#FILE SETTINGS
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024,

	#KEY SETTINGS
	SECRET_KEY = 'super_secret_key'
	)


@app.route('/')
def index():
	return render_template('index.html')


'''
	work directory render fucntion.

'''
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


'''
	email functions.
'''
@app.route('/email', methods=['POST', 'GET'])
def send_email_button():
	if request.method == 'POST':
		first_name = request.form['fname']
		last_name = request.form['lname']
		sender_email = request.form['sender']
		subject = request.form['subject']
		message_content = request.form['message']

		email_info = []
		email_info.append(first_name)
		email_info.append(last_name)
		email_info.append(sender_email)
		email_info.append(subject)
		email_info.append(message_content)

		'''
			spam protection.
		'''

		if ('' in email_info):
			flash('Please fill out all forms', 'error')
			email_info = []
			return redirect('/')

		tmp_cnt = 0

		for v in list(set(email_info)):
			tmp_cnt = email_info.count(v)

			if (tmp_cnt > 1):
				flash('Invalid Input', 'error')
				email_info = []
				return redirect('/')



		result = send_email(first_name, last_name, sender_email, subject, message_content)
		email_info = []


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
		msg.body = 'first name:\t\t' + first_name + '\n' + 'last name:\t\t' + last_name + '\n' + 'sender:\t\t' + sender_email + '\n' + 'content:\t' + message_content
		mail.send(msg)
	except Exception:
		print('email system error:')
		pass
	finally:
		pass


'''
	image processing.
'''
@app.route('/image_upload', methods=['POST', 'GET'])
def upload_file():
	if request.method == 'POST':
		try:
			f = request.files['file']
			f.save(secure_filename(f.filename))
			return redirect('/work/image-processing')
		except Exception:
			return 'fail to upload image file'
			pass
		finally:
			pass


'''
	main.
'''
if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80, debug = True)
