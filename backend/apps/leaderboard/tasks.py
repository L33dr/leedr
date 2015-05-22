from __future__ import absolute_import
from django.core.mail import EmailMessage
from requests import get
import yaml
from leaderboard.settings import EMAIL_HOST_USER, LOL_API_KEY
from django.template import Context, loader
from celery import shared_task


"""
Shared tasks can be called throughout the application and ran asynchronously by importing the task name,
    then calling taskname.delay(parameters). The delay function will add it into the queue to be processed as soon as possible.

For more information see: https://celery.readthedocs.org/en/latest/userguide/calling.html

You can also call a shared task directly and have it executed in a serial manor by just calling it as if were any other function.
"""

@shared_task()
def get_LOL_id_by_username(username):
    """
    Returns LOL ID by performing a query on their api by LOL username.
    This would generally be ran right as a user requests we add their game.
    """
    request_URL = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + username + '?api_key=' + LOL_API_KEY
    request = get(request_URL)
    if request.status_code not in [400, 404, 500]:
        data = yaml.load(request.content)
        return data[username]['id']
    elif request.status_code == 404:
        raise NameError("API returned 404. Name not found or is incorrect")
    else:
        raise Exception("LOL API returned status code: {} ".format(request.status_code))


@shared_task()
def send_contact_request_reply_task(first_name, email):
    """

    """
    template = loader.get_template('leaderboard/email.html')
    context = Context({"first_name": first_name})
    message = template.render(context)

    subject = "Thank you for submitting the form."
    from_emails = EMAIL_HOST_USER
    msg = EmailMessage(subject, message, from_emails, [email])
    msg.content_subtype = "html"
    msg.send()

@shared_task()
def send_contact_request_alert_task(first_name, reply_email, comment, ip_address):
    """
    Alerting the admin that there was a new comment.
    """
    subject = "New contact request."
    from_email = EMAIL_HOST_USER
    message = "<html>A new contact requests has been submitted. <br><br>Name: {}<br>Email: {}<br>Message: {}" \
              "<br>IP Address: {}<br></html>".format(first_name, reply_email, comment, ip_address)
    msg = EmailMessage(subject, message, from_email, [EMAIL_HOST_USER])
    msg.content_subtype = 'html'
    msg.send()

