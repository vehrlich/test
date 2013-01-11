import urllib2
import simplejson

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from accounts.models import Account
from accounts.models import Referral
from accounts.models import MailingList

class Command(BaseCommand):
    help = 'Update database with server data'

    def handle(self, *args, **options):
        """
        Get JSON response from server, parse it and save to the database
        """
        #create url with headers and get response from request
        req = urllib2.Request(
            "%s?username=%s&api_key=%s" % 
            (settings.NL_SETTINGS['url'], settings.NL_SETTINGS['username'],
             settings.NL_SETTINGS['api_key'])
            )
        
        req.add_header('Accept','application/json')
        req.add_header('Content-Type','application/json')
        
        opener = urllib2.build_opener()
        f = opener.open(req)
        server_data = simplejson.load(f)
        
        #data from server contents meta information and objects
        for object_data in server_data['objects']:
            referral = Referral()
            referral.name = object_data['tr_referral']['name']
            referral.resource_uri = object_data['tr_referral']['resource_uri']
            referral.save()

            account = Account()
            account.birth_date = object_data['birth_date']
            account.city = object_data['city']
            account.email = object_data['email']
            account.first_name = object_data['first_name']
            account.gender = object_data['gender']
            account.last_name = object_data['last_name']
            account.lead = object_data['lead']
            account.last_name = object_data['last_name']
            account.phone = object_data['phone']
            account.resource_uri = object_data['resource_uri']
            account.street_number = object_data['street_number']
            account.tr_input_method = object_data['tr_input_method']
            account.ip_address = object_data['ip_address']
            account.tr_language = object_data['tr_language']
            account.utm_campaign = object_data['utm_campaign']
            account.utm_medium = object_data['utm_medium']
            account.utm_medium = object_data['utm_source']
            account.utm_medium = object_data['zipcode']
            account.tr_referral = referral
            account.save_from_server()
            
            for mailing_list_data in object_data['mailing_lists']:
                mailing_list = MailingList()
                mailing_list.name = mailing_list_data['name']
                mailing_list.resource_uri = mailing_list_data['resource_uri']
                mailing_list.save()
                account.mailing_lists.add(mailing_list)
            
            account.save_from_server()
        
