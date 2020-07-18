from datetime import datetime
from os.path import splitext
from django.http import HttpResponseForbidden
from django.core.signing import Signer
from django.template.loader import render_to_string



def get_timestamp_path(instance, filename):
	return f'{datetime.now().timestamp()}{splitext(filename)[1]}'

def send_activation_notification(user):
	if ALLOWED_HOSTS:
		host = 'http://' + ALLOWED_HOSTS[0]
	else:
		host = 'http://localhost:8000'
	context = {'user' : user, 'host' : host, 'sign' : Signer.sign(user.username)} # Последнее это мы шифруем индефикатор, чтобы он был учстойив к подделке
	subject = render_to_string('email/al_subj.txt', context)
	body = render_to_string('email/al_body.txt', context)
	user.email_user(subject, body)
