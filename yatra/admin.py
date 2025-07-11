from django.contrib import admin
from  .models import Destination,Detailed_desc, pessanger_detail, Transactions, Contact
# Register your models here.

admin.site.register(Destination)
admin.site.register(Detailed_desc)
admin.site.register(pessanger_detail)
admin.site.register(Transactions)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message')

