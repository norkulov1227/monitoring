from django.contrib import admin
from .models import Monitoring

@admin.register(Monitoring)
class MonitoringAdmin(admin.ModelAdmin):
    list_display = ('user','status', "payment_type", 'comment', 'price', 'created_at',)
    search_fields = ('comment', )
    list_filter = ('created_at', 'status', 'user')
    
