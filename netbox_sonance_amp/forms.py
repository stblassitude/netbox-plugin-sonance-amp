from django import forms

from dcim.models import Interface
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from .choices import (
    AmpParameterTypeChoices, ModeSource2Choices, OutputGroupChoices, OutputSourceChoices, StereoModeChoices,
)
from .models import AmpInputSettings, AmpOutputSettings


class AmpInputSettingsForm(NetBoxModelForm):
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
    )

    fieldsets = (
        FieldSet('interface', 'level_trim_db', name='Input Settings'),
    )

    class Meta:
        model = AmpInputSettings
        fields = ('interface', 'level_trim_db', 'tags')


class AmpOutputSettingsForm(NetBoxModelForm):
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
    )

    fieldsets = (
        FieldSet('interface', name='Interface'),
        FieldSet('stereo_mono', 'dsp_preset', 'output_group', 'bridge_mode', name='Output Setup'),
        FieldSet('output_source_1', 'output_source_2', 'mode_source_2', name='Output Source'),
        FieldSet('output_volume', 'turn_on_volume', 'maximum_volume', 'gain_offset', 'mute', name='Output Volume'),
    )

    class Meta:
        model = AmpOutputSettings
        fields = (
            'interface', 'stereo_mono', 'dsp_preset', 'output_group', 'bridge_mode',
            'output_source_1', 'output_source_2', 'mode_source_2',
            'output_volume', 'turn_on_volume', 'maximum_volume', 'gain_offset', 'mute', 'tags',
        )
        widgets = {
            'gain_offset': forms.NumberInput(attrs={'step': '0.5'}),
        }


class AmpParameterForm(forms.Form):
    """
    Combined form used from an Interface's detail page to choose whether it carries no amp
    parameters, input amp parameters, or output amp parameters, and to edit whichever
    parameter set applies.
    """
    parameter_type = forms.ChoiceField(
        label='Amp parameters',
        choices=AmpParameterTypeChoices,
    )

    # AmpInputSettings fields
    level_trim_db = forms.DecimalField(
        label='Level trim (dB)', max_digits=4, decimal_places=1, min_value=-18, max_value=18, required=False,
    )

    # AmpOutputSettings fields
    stereo_mono = forms.ChoiceField(choices=StereoModeChoices, required=False)
    dsp_preset = forms.CharField(max_length=100, required=False)
    output_group = forms.ChoiceField(choices=OutputGroupChoices, required=False)
    bridge_mode = forms.BooleanField(required=False)
    output_source_1 = forms.ChoiceField(choices=OutputSourceChoices, required=False)
    output_source_2 = forms.ChoiceField(choices=OutputSourceChoices, required=False)
    mode_source_2 = forms.ChoiceField(choices=ModeSource2Choices, required=False)
    output_volume = forms.DecimalField(
        max_digits=4, decimal_places=1, min_value=-70, max_value=12, required=False,
    )
    turn_on_volume = forms.DecimalField(
        max_digits=4, decimal_places=1, min_value=-70, max_value=12, required=False,
    )
    maximum_volume = forms.DecimalField(
        max_digits=4, decimal_places=1, min_value=-70, max_value=12, required=False,
    )
    gain_offset = forms.DecimalField(
        max_digits=3, decimal_places=1, min_value=-6, max_value=6, required=False,
        widget=forms.NumberInput(attrs={'step': '0.5'}),
    )
    mute = forms.BooleanField(required=False)
