from django.contrib import admin
from piccolo.models import Buyers, PreviousOrders, Transactions
# Register your models here.
admin.site.register(Buyers)
admin.site.register(PreviousOrders)
admin.site.register(Transactions)
