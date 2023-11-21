from healthapp import app
from flask.signals import Namespace

app_signal=Namespace()


""" signals for email notifications on daily medication notification """
contact_signal = app_signal.signal('contact')
