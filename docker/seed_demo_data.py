from dcim.choices import DeviceStatusChoices, InterfaceTypeChoices
from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site

from netbox_plugin_sonance_amp.models import AmpInputSettings

site, _ = Site.objects.get_or_create(slug='demo-site', defaults={'name': 'Demo Site'})
manufacturer, _ = Manufacturer.objects.get_or_create(slug='sonance', defaults={'name': 'Sonance'})
device_type, _ = DeviceType.objects.get_or_create(
    manufacturer=manufacturer, slug='sonamp', defaults={'model': 'SonAmp'},
)
device_role, _ = DeviceRole.objects.get_or_create(slug='amplifier', defaults={'name': 'Amplifier'})

device, created = Device.objects.get_or_create(
    name='sonamp-1',
    site=site,
    defaults={
        'device_type': device_type,
        'role': device_role,
        'status': DeviceStatusChoices.STATUS_ACTIVE,
    },
)

# A SonAmp has 4 stereo input pairs and 4 stereo output pairs.
channels = [f'{number}{side}' for number in range(1, 5) for side in ('L', 'R')]

input_interfaces = []
for channel in channels:
    label = f'In {channel}'
    interface, _ = Interface.objects.get_or_create(
        device=device, name=label, defaults={'type': InterfaceTypeChoices.TYPE_OTHER, 'label': label},
    )
    AmpInputSettings.objects.get_or_create(interface=interface)
    input_interfaces.append(interface)

output_interfaces = []
for channel in channels:
    label = f'Speaker {channel}'
    interface, _ = Interface.objects.get_or_create(
        device=device, name=label, defaults={'type': InterfaceTypeChoices.TYPE_OTHER, 'label': label},
    )
    output_interfaces.append(interface)

print(f'Demo device: {device} (id={device.pk})')
print(f'Input interfaces: {", ".join(i.name for i in input_interfaces)}')
print(f'Output interfaces: {", ".join(i.name for i in output_interfaces)}')
