from django.contrib import admin

from .models import AmpInputSettings, AmpOutputSettings


@admin.register(AmpInputSettings)
class AmpInputSettingsAdmin(admin.ModelAdmin):
    list_display = ('interface', 'level_trim_db')


@admin.register(AmpOutputSettings)
class AmpOutputSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'interface', 'stereo_mono', 'dsp_preset', 'output_group', 'bridge_mode', 'output_volume', 'mute',
    )
