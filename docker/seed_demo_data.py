from dcim.choices import DeviceStatusChoices, InterfaceTypeChoices
from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site

from netbox_plugin_sonance_amp.models import AmpInputSettings, AmpOutputSettings

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

# A SonAmp has 4 stereo input pairs and 4 stereo output pairs. The interface name is the
# amp's fixed physical channel designation; the label is the zone name assigned to it.
input_labels = {
    '1L': '1 Library', '1R': '1 Library',
    '2L': '2 Great', '2R': '2 Great',
    '3L': '3 Patio', '3R': '3 Patio',
    '4L': '4 Upstairs', '4R': '4 Upstairs',
}
output_labels = {
    '1L': 'Library E L', '1R': 'Library E R',
    '2L': 'Library W L', '2R': 'Library W R',
    '3L': 'Library Sub', '3R': 'Output 3R',
    '4L': 'Great Bar L', '4R': 'Great Bar R',
}

input_interfaces = []
input_interfaces_by_channel = {}
for channel, label in input_labels.items():
    name = f'In {channel}'
    interface, _ = Interface.objects.get_or_create(
        device=device, name=name, defaults={'type': InterfaceTypeChoices.TYPE_OTHER, 'label': label},
    )
    AmpInputSettings.objects.get_or_create(interface=interface)
    input_interfaces.append(interface)
    input_interfaces_by_channel[channel] = interface

# Each output pair is fed by an input pair; outputs 1-3 all draw on the Library input,
# output 4 draws on the Great room input.
output_sources = {
    '1L': '1L', '1R': '1R',
    '2L': '1L', '2R': '1R',
    '3L': '1L', '3R': '1R',
    '4L': '2L', '4R': '2R',
}

output_interfaces = []
for channel, label in output_labels.items():
    name = f'Speaker {channel}'
    interface, _ = Interface.objects.get_or_create(
        device=device, name=name, defaults={'type': InterfaceTypeChoices.TYPE_OTHER, 'label': label},
    )
    AmpOutputSettings.objects.get_or_create(
        interface=interface,
        defaults={'output_source_1': input_interfaces_by_channel[output_sources[channel]]},
    )
    output_interfaces.append(interface)

print(f'Demo device: {device} (id={device.pk})')
print(f'Input interfaces: {", ".join(f"{i.name} ({i.label})" for i in input_interfaces)}')
print(f'Output interfaces: {", ".join(f"{i.name} ({i.label})" for i in output_interfaces)}')
