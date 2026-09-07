from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site

from netbox_plugin_sonance_amp.forms import AmpParameterForm
from netbox_plugin_sonance_amp.models import AmpInputSettings
from netbox_plugin_sonance_amp.views import InterfaceAmpParametersEditView


class InterfaceAmpParametersEditViewTestCase(TestCase):

    def setUp(self):
        site = Site.objects.create(name='Site 1', slug='site-1')
        manufacturer = Manufacturer.objects.create(name='Sonance', slug='sonance')
        device_type = DeviceType.objects.create(manufacturer=manufacturer, model='SonAmp', slug='sonamp')
        device_role = DeviceRole.objects.create(name='Amplifier', slug='amplifier')

        device_a = Device.objects.create(name='amp-a', site=site, device_type=device_type, role=device_role)
        device_b = Device.objects.create(name='amp-b', site=site, device_type=device_type, role=device_role)

        self.local_input = Interface.objects.create(device=device_a, name='In 1L', type='other')
        self.remote_input = Interface.objects.create(device=device_b, name='In 1L', type='other')
        self.output = Interface.objects.create(device=device_a, name='Out 1L', type='other')

        AmpInputSettings.objects.create(interface=self.local_input)
        AmpInputSettings.objects.create(interface=self.remote_input)

    def test_output_source_choices_limited_to_same_device_excluding_self(self):
        form = AmpParameterForm()
        InterfaceAmpParametersEditView().limit_output_sources(form, self.output)

        choices = list(form.fields['output_source_1'].queryset)
        self.assertIn(self.local_input, choices)
        self.assertNotIn(self.remote_input, choices)
        self.assertNotIn(self.output, choices)
