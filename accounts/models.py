import requests

from django.conf import settings
from django.db import models
from django.core import serializers

class Account(models.Model):
    first_name = models.CharField(verbose_name="First name", max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last name", max_length=50, null=True, blank=True)
    email = models.CharField(verbose_name='Email', primary_key=True, max_length=50)
    street_number = models.CharField(verbose_name="Street number", max_length=20, null=True, blank=True)
    birth_date = models.DateField(verbose_name="Birth date", null=True, blank=True)
    city = models.CharField(verbose_name="City", max_length=50, null=True, blank=True)
    country = models.CharField(verbose_name="Country", max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=(('m', 'male'), ('f', 'female')), default='m')
    phone = models.CharField(verbose_name="Phone", max_length=50, null=True, blank=True)
    zipcode = models.CharField(verbose_name="ZIP code", max_length=20, null=True, blank=True)
    resource_uri = models.CharField(verbose_name="Resource URI", max_length=50, null=True, blank=True)
    mailing_lists = models.ManyToManyField('MailingList', verbose_name="Mailing lists", null=True, blank=True)
    tr_input_method = models.CharField(verbose_name="Input method", max_length=20, null=True, blank=True)
    tr_referral = models.ForeignKey('Referral', verbose_name="Referral", null=False, blank=False)
    ip_address = models.IPAddressField(verbose_name="IP address", null=False, blank=False)
    tr_language = models.CharField(verbose_name="Language", max_length=5, null=True, blank=True)
    utm_campaign = models.CharField(verbose_name="UTM Campaign", max_length=100, null=True, blank=True)
    utm_medium = models.CharField(verbose_name="UTM Medium", max_length=100, null=True, blank=True)
    utm_source = models.CharField(verbose_name="UTM Source", max_length=100, null=True, blank=True)
    lead = models.BooleanField(verbose_name="Lead", default=False)
        
    def __str__(self):
        return "%s %s" % (self.last_name, self.first_name)
    
    def save_from_server(self, *args,  **kwargs):
        """
        It's just an easy save method. But without lead parameter check
        It's used after DB data mining
        """
        super(Account, self).save(*args,  **kwargs)
    
    def save(self, *args,  **kwargs):
        """
        Override save method. After save send data to server.
        Lead parameter is set to False.

        return: error code of POST HTTP request
        """
        #after edit record is not lead
        if self.lead:
            self.lead = False
        
        super(Account, self).save(*args,  **kwargs)    
        serialize_output = serializers.serialize('json', [self], use_natural_keys=True)

        #serialize output has parts which server do not accept, send only fields
        start_pos = serialize_output.find("fields") + 10
        cut_serialize_output = serialize_output[start_pos:len(serialize_output)-2]
        #email is as pk in string output. So add email to string
        cut_serialize_output = '{"email":"%s", %s' % (self.email, cut_serialize_output)
        #ok another hack. Server script could not handle more mailing lists.
        #so every outgoing object will have 'mailing_list':'2'
        start_cut = cut_serialize_output.find("[")
        end_cut = cut_serialize_output.find("]") + 1 
        
        cut_serialize_output = "".join([cut_serialize_output[0:start_cut], 
                                        '2', 
                                        cut_serialize_output[end_cut:len(cut_serialize_output)]]) 
        
        #send data to server
        url = "%s?username=%s\&api_key=%s" % (
            settings.NL_SETTINGS['url'], settings.NL_SETTINGS['username'], 
            settings.NL_SETTINGS['api_key'])
        
        headers = {'Content-Type': 'application/json', 
                   'Accept': 'application/json'}

        try:
            req = requests.post(url, data=cut_serialize_output, headers=headers)
            req.raise_for_status()
        except:
            #TODO add HTTPError etc.
            pass
        
        #try to catch bad status codes (authorization, etc)
        try:
            req.raise_for_status()
        except:
            #only pass - error message will be shown to user, data are saved
            #only locally
            pass

        return req.status_code
    #enddef

#endclass

class Referral(models.Model):
    name=models.CharField(verbose_name="Name", primary_key=True, max_length=20)
    resource_uri=models.CharField(verbose_name="Resource URI", max_length=100)
    
    def __str__(self):
        return self.name
    
    def natural_key(self):
        return self.name
#endclass

class MailingList(models.Model):
    name=models.CharField(verbose_name="Name", primary_key=True, max_length=100)
    resource_uri=models.CharField(verbose_name="Resource URI", max_length=100)
    
    def natural_key(self):
        return self.name
    
    def __str__(self):
        return self.name
#endclass
