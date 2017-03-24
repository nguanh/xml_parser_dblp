from django.contrib import admin
from .models import Schedule,Config
from django_celery_beat.admin import TaskChoiceField
from django import forms
# Register your models here.
from django_admin_row_actions import AdminRowActionsMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from kombu.utils.json import loads

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

class ConfigForm(forms.ModelForm):
    """Form that lets you create and modify periodic tasks."""

    regtask = TaskChoiceField(
        label=_('Task (registered)'),
        required=False,
    )

    class Meta:
        """Form metadata."""

        model = Config
        exclude = ()

    def clean(self):
        # set task as the data from regtask
        data = super(ConfigForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                _('Unable to parse JSON: %s') % exc,
            )
        return value

    def clean_extra_config(self):
        return self._clean_json('extra_config')

    def clean_task_parameter(self):
        return self._clean_json('task_parameter')


class ConfigAdmin(AdminRowActionsMixin,admin.ModelAdmin):
    form = ConfigForm
    model = Config
    # welche attribute sollen in der listenansicht gezeigt werden
    list_display = ('__str__', 'enabled','task')
    """Admin-interface for Harvester Configs."""
    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Log',
                #'url': reverse('Harvester:config_log', args=[obj.id]),
                'url':"http://google.de",
                'enabled': True,
                'tooltip': "Display Harvester Log"
            }
        ]
        row_actions += super(ConfigAdmin, self).get_row_actions(obj)
        return row_actions

    fieldsets = (
        (None, {
            'fields': ('name', 'table_name', 'url', 'enabled', 'limit', 'extra_config'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('schedule', 'regtask','task_parameter'),
            'classes': ('extrapretty', 'wide', ),
        }),
    )

admin.site.register(Schedule)
admin.site.register(Config, ConfigAdmin)
