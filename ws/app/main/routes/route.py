from flask_restplus import Resource, Namespace, reqparse
from flask import render_template, make_response
from werkzeug.datastructures import FileStorage

from ..service import subscriptionService
from ..form.user_form import SubscriptionForm, UnsubscriptionForm

api = Namespace('sns', description='Notifications')

@api.route('/subscribe')
class SubscribeSNSForm(Resource):
    def get(self):
        form = SubscriptionForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('subscribe.html', title='Subscribe', form=form), 200, headers)

    def post(self):
        headers = {'Content-Type': 'text/html'}
        form = SubscriptionForm()
        email = form.email.data
        if '@' not in email and '.' not in email:
            return make_response(render_template('response.html', title='Subscribe'), 200, headers)
        subscriptionService.subscribe(email)
        return make_response(render_template('response.html', title='Subscribe'), 200, headers)


@api.route('/unsubscribe')
class UnsubscribeSNSForm(Resource):
    def get(self):
        form = UnsubscriptionForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('subscribe.html', title='Unsubscribe', form=form), 200, headers)


    def post(self):
        headers = {'Content-Type': 'text/html'}
        form = UnsubscriptionForm()
        email = form.email.data
        if '@' not in email and '.' not in email:
            return make_response(render_template('response.html', title='Subscribe'), 200, headers)
        subscriptionService.unsubscribe(email)
        return make_response(render_template('response.html', title='Subscribe'), 200, headers)
