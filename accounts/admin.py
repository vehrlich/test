from django.contrib import admin

from accounts.models import Account
from accounts.models import Referral
from accounts.models import MailingList

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name')
    
    fieldsets = [
        ('Account', {'fields': ['first_name', 'last_name', 'email', 'street_number', 'city', 'zipcode', 'country', 'phone', 'birth_date', 'gender', 'mailing_lists', 'resource_uri']}),
        ('TR', {'fields': ['tr_input_method', 'tr_referral', 'tr_ip_address', 'tr_language'], 'classes': ['collapse']}),
        ('UTM',{'fields': ['utm_campaign', 'utm_medium', 'utm_source'], 'classes': ['collapse']}),
        ('', {'fields': ['lead']})
    ]
    readonly_fields = ('lead',)
 
admin.site.register(Account, AccountAdmin)
admin.site.register(Referral)
admin.site.register(MailingList)