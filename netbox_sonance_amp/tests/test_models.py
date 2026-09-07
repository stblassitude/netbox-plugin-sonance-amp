from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site

from netbox_sonance_amp.choices import OutputGroupChoices, StereoModeChoices
from netbox_sonance_amp.models import AmpInputSettings, AmpOutputSettings


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
