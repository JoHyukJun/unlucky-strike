from flask import Flask, render_template, request
import sys
import os

app = Flask(__name__)

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



if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 80, debug = True)