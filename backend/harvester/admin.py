from django.contrib import admin
from .models import Schedule,Config
# Register your models here.
from django_admin_row_actions import AdminRowActionsMixin
from django.urls import reverse

"""
class ConfigAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Log',
                'url': reverse('Harvester:config_log', args=[obj.id]),
                'enabled': True,
                'tooltip': "Display Harvester Log"
            }
        ]
        row_actions += super(ConfigAdmin, self).get_row_actions(obj)
        return row_actions


admin.site.register(Config, ConfigAdmin)
"""
admin.site.register(Schedule)
admin.site.register(Config)
