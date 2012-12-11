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
    tr_ip_address = models.IPAddressField(verbose_name="IP address", null=True, blank=True)
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
        print(cut_serialize_output)
        #TODO send data to server
#endclass

class Referral(models.Model):
    name=models.CharField(verbose_name="Name", primary_key=True, max_length=20)
    resource_uri=models.CharField(verbose_name="Resource URI", max_length=100)
    
    def __str__(self):
        return self.name
    
    def natural_key(self):
        return {'name':self.name, 'resource_uri':self.resource_uri}
    
#endclass

class MailingList(models.Model):
    #objects = MailingListManager()
    
    name=models.CharField(verbose_name="Name", primary_key=True, max_length=100)
    resource_uri=models.CharField(verbose_name="Resource URI", max_length=100)
    
    def natural_key(self):
        return {'name':self.name, 'resource_uri':self.resource_uri}
    
    def __str__(self):
        return self.name
    
    #class Meta:
    #    unique_together = (('name', 'resource_uri'),)
#endclass
