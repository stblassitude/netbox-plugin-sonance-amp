from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site

from netbox_plugin_sonance_amp.choices import OutputGroupChoices, StereoModeChoices
from netbox_plugin_sonance_amp.forms import AmpInputInterfaceChoiceField, amp_input_interfaces
from netbox_plugin_sonance_amp.models import AmpInputSettings, AmpOutputSettings


class AmpSettingsTestCase(TestCase):

    def setUp(self):
        site = Site.objects.create(name='Site 1', slug='site-1')
        manufacturer = Manufacturer.objects.create(name='Sonance', slug='sonance')
        device_type = DeviceType.objects.create(manufacturer=manufacturer, model='SonAmp', slug='sonamp')
        device_role = DeviceRole.objects.create(name='Amplifier', slug='amplifier')
        device = Device.objects.create(
            name='amp-1', site=site, device_type=device_type, role=device_role,
        )
        self.input_interface = Interface.objects.create(device=device, name='Input 1', type='other')
        self.output_interface = Interface.objects.create(device=device, name='Output 1', type='other')

    def test_create_input_settings(self):
        settings = AmpInputSettings.objects.create(interface=self.input_interface, level_trim_db=-3)

        self.assertEqual(settings.interface, self.input_interface)
        self.assertEqual(self.input_interface.sonance_amp_input_settings, settings)
        self.assertIn(str(self.input_interface), str(settings))

    def test_create_output_settings(self):
        settings = AmpOutputSettings.objects.create(
            interface=self.output_interface,
            stereo_mono=StereoModeChoices.MONO,
            dsp_preset='Living Room',
            output_group=OutputGroupChoices.CHOICES[0][0],
        )

        self.assertEqual(settings.interface, self.output_interface)
        self.assertEqual(self.output_interface.sonance_amp_output_settings, settings)
        self.assertEqual(settings.turn_on_volume, -70)
        self.assertFalse(settings.mute)

    def test_interface_carries_at_most_one_settings_type(self):
        AmpInputSettings.objects.create(interface=self.input_interface)

        self.assertIsNone(getattr(self.input_interface, 'sonance_amp_output_settings', None))

    def test_output_source_selectable_only_from_configured_inputs(self):
        # Not yet configured with AmpInputSettings: not a valid source.
        self.assertNotIn(self.input_interface, amp_input_interfaces())

        AmpInputSettings.objects.create(interface=self.input_interface)

        self.assertIn(self.input_interface, amp_input_interfaces())
        self.assertNotIn(self.output_interface, amp_input_interfaces())

    def test_output_source_label_prefers_label_over_name(self):
        AmpInputSettings.objects.create(interface=self.input_interface)
        field = AmpInputInterfaceChoiceField(queryset=amp_input_interfaces())

        self.assertEqual(field.label_from_instance(self.input_interface), 'Input 1')

        self.input_interface.label = 'In 1L'
        self.input_interface.save()

        self.assertEqual(field.label_from_instance(self.input_interface), 'In 1L')

    def test_output_settings_output_source(self):
        AmpInputSettings.objects.create(interface=self.input_interface)
        settings = AmpOutputSettings.objects.create(
            interface=self.output_interface,
            output_source_1=self.input_interface,
        )

        self.assertEqual(settings.output_source_1, self.input_interface)
        self.assertIsNone(settings.output_source_2)
