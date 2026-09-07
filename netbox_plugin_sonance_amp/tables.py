import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import BooleanColumn, ChoiceFieldColumn, TagColumn

from .models import AmpInputSettings, AmpOutputSettings


class AmpInputSettingsTable(NetBoxTable):
    interface = tables.Column(linkify=True)
    device = tables.Column(accessor='interface__device', linkify=True)
    tags = TagColumn(url_name='plugins:netbox_plugin_sonance_amp:ampinputsettings_list')

    class Meta(NetBoxTable.Meta):
        model = AmpInputSettings
        fields = ('pk', 'id', 'interface', 'device', 'level_trim_db', 'tags', 'created', 'last_updated')
        default_columns = ('pk', 'interface', 'device', 'level_trim_db')


class AmpOutputSettingsTable(NetBoxTable):
    interface = tables.Column(linkify=True)
    device = tables.Column(accessor='interface__device', linkify=True)
    stereo_mono = ChoiceFieldColumn()
    output_group = ChoiceFieldColumn()
    output_source_1 = ChoiceFieldColumn()
    output_source_2 = ChoiceFieldColumn()
    mode_source_2 = ChoiceFieldColumn()
    bridge_mode = BooleanColumn()
    mute = BooleanColumn()
    tags = TagColumn(url_name='plugins:netbox_plugin_sonance_amp:ampoutputsettings_list')

    class Meta(NetBoxTable.Meta):
        model = AmpOutputSettings
        fields = (
            'pk', 'id', 'interface', 'device', 'stereo_mono', 'dsp_preset', 'output_group', 'bridge_mode',
            'output_source_1', 'output_source_2', 'mode_source_2', 'output_volume', 'turn_on_volume',
            'maximum_volume', 'gain_offset', 'mute', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'interface', 'device', 'stereo_mono', 'dsp_preset', 'output_group', 'mute')
