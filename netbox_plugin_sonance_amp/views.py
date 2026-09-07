from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from dcim.models import Interface
from netbox.views import generic

from .choices import AmpParameterTypeChoices
from .filtersets import AmpInputSettingsFilterSet, AmpOutputSettingsFilterSet
from .forms import AmpInputSettingsForm, AmpOutputSettingsForm, AmpParameterForm
from .models import AmpInputSettings, AmpOutputSettings
from .tables import AmpInputSettingsTable, AmpOutputSettingsTable


#
# AmpInputSettings
#

class AmpInputSettingsListView(generic.ObjectListView):
    queryset = AmpInputSettings.objects.all()
    table = AmpInputSettingsTable
    filterset = AmpInputSettingsFilterSet


class AmpInputSettingsView(generic.ObjectView):
    queryset = AmpInputSettings.objects.all()


class AmpInputSettingsEditView(generic.ObjectEditView):
    queryset = AmpInputSettings.objects.all()
    form = AmpInputSettingsForm


class AmpInputSettingsDeleteView(generic.ObjectDeleteView):
    queryset = AmpInputSettings.objects.all()


#
# AmpOutputSettings
#

class AmpOutputSettingsListView(generic.ObjectListView):
    queryset = AmpOutputSettings.objects.all()
    table = AmpOutputSettingsTable
    filterset = AmpOutputSettingsFilterSet


class AmpOutputSettingsView(generic.ObjectView):
    queryset = AmpOutputSettings.objects.all()


class AmpOutputSettingsEditView(generic.ObjectEditView):
    queryset = AmpOutputSettings.objects.all()
    form = AmpOutputSettingsForm


class AmpOutputSettingsDeleteView(generic.ObjectDeleteView):
    queryset = AmpOutputSettings.objects.all()


#
# Combined interface amp parameter editor
#

class InterfaceAmpParametersEditView(PermissionRequiredMixin, View):
    """
    Presents a single form, reached from an Interface's detail page, for choosing whether the
    interface carries no amp parameters, input amp parameters, or output amp parameters, and for
    editing whichever parameter set applies. Saving swaps out the underlying AmpInputSettings /
    AmpOutputSettings row(s) to match the selected type.
    """
    permission_required = 'dcim.change_interface'

    def get_initial(self, interface):
        input_settings = getattr(interface, 'sonance_amp_input_settings', None)
        output_settings = getattr(interface, 'sonance_amp_output_settings', None)

        if input_settings:
            return {
                'parameter_type': AmpParameterTypeChoices.INPUT,
                'level_trim_db': input_settings.level_trim_db,
            }
        if output_settings:
            return {
                'parameter_type': AmpParameterTypeChoices.OUTPUT,
                'stereo_mono': output_settings.stereo_mono,
                'dsp_preset': output_settings.dsp_preset,
                'output_group': output_settings.output_group,
                'bridge_mode': output_settings.bridge_mode,
                'output_source_1': output_settings.output_source_1,
                'output_source_2': output_settings.output_source_2,
                'mode_source_2': output_settings.mode_source_2,
                'output_volume': output_settings.output_volume,
                'turn_on_volume': output_settings.turn_on_volume,
                'maximum_volume': output_settings.maximum_volume,
                'gain_offset': output_settings.gain_offset,
                'mute': output_settings.mute,
            }
        return {'parameter_type': AmpParameterTypeChoices.NONE}

    def get(self, request, interface_id):
        interface = get_object_or_404(Interface, pk=interface_id)
        form = AmpParameterForm(initial=self.get_initial(interface))
        return render(request, 'netbox_plugin_sonance_amp/amp_parameters_edit.html', {
            'object': interface,
            'interface': interface,
            'form': form,
            'return_url': interface.get_absolute_url(),
        })

    def post(self, request, interface_id):
        interface = get_object_or_404(Interface, pk=interface_id)
        form = AmpParameterForm(data=request.POST)

        if form.is_valid():
            parameter_type = form.cleaned_data['parameter_type']

            if parameter_type != AmpParameterTypeChoices.INPUT:
                AmpInputSettings.objects.filter(interface=interface).delete()
            if parameter_type != AmpParameterTypeChoices.OUTPUT:
                AmpOutputSettings.objects.filter(interface=interface).delete()

            if parameter_type == AmpParameterTypeChoices.INPUT:
                AmpInputSettings.objects.update_or_create(
                    interface=interface,
                    defaults={
                        'level_trim_db': form.cleaned_data['level_trim_db'] or 0,
                    },
                )
            elif parameter_type == AmpParameterTypeChoices.OUTPUT:
                AmpOutputSettings.objects.update_or_create(
                    interface=interface,
                    defaults={
                        'stereo_mono': form.cleaned_data['stereo_mono'],
                        'dsp_preset': form.cleaned_data['dsp_preset'],
                        'output_group': form.cleaned_data['output_group'],
                        'bridge_mode': form.cleaned_data['bridge_mode'],
                        'output_source_1': form.cleaned_data['output_source_1'],
                        'output_source_2': form.cleaned_data['output_source_2'],
                        'mode_source_2': form.cleaned_data['mode_source_2'],
                        'output_volume': form.cleaned_data['output_volume'] or 0,
                        'turn_on_volume': form.cleaned_data['turn_on_volume'] or 0,
                        'maximum_volume': form.cleaned_data['maximum_volume'] or 0,
                        'gain_offset': form.cleaned_data['gain_offset'] or 0,
                        'mute': form.cleaned_data['mute'],
                    },
                )

            return redirect(interface.get_absolute_url())

        return render(request, 'netbox_plugin_sonance_amp/amp_parameters_edit.html', {
            'object': interface,
            'interface': interface,
            'form': form,
            'return_url': interface.get_absolute_url(),
        })
