from dcim.api.serializers import InterfaceSerializer
from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer

from ..choices import ModeSource2Choices, OutputGroupChoices, OutputSourceChoices, StereoModeChoices
from ..models import AmpInputSettings, AmpOutputSettings


class AmpInputSettingsSerializer(NetBoxModelSerializer):
    interface = InterfaceSerializer(nested=True)

    class Meta:
        model = AmpInputSettings
        fields = (
            'id', 'url', 'display', 'interface', 'level_trim_db', 'tags', 'custom_fields', 'created',
            'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'interface', 'level_trim_db')


class AmpOutputSettingsSerializer(NetBoxModelSerializer):
    interface = InterfaceSerializer(nested=True)
    stereo_mono = ChoiceField(choices=StereoModeChoices)
    output_group = ChoiceField(choices=OutputGroupChoices, required=False)
    output_source_1 = ChoiceField(choices=OutputSourceChoices, required=False)
    output_source_2 = ChoiceField(choices=OutputSourceChoices, required=False)
    mode_source_2 = ChoiceField(choices=ModeSource2Choices, required=False)

    class Meta:
        model = AmpOutputSettings
        fields = (
            'id', 'url', 'display', 'interface', 'stereo_mono', 'dsp_preset', 'output_group', 'bridge_mode',
            'output_source_1', 'output_source_2', 'mode_source_2', 'output_volume', 'turn_on_volume',
            'maximum_volume', 'gain_offset', 'mute', 'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'interface', 'stereo_mono', 'dsp_preset')
