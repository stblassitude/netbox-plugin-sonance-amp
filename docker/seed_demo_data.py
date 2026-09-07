from dcim.choices import DeviceStatusChoices, InterfaceTypeChoices
from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site

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

input_interface, _ = Interface.objects.get_or_create(
    device=device, name='Input 1', defaults={'type': InterfaceTypeChoices.TYPE_OTHER},
)
output_interface, _ = Interface.objects.get_or_create(
    device=device, name='Output 1', defaults={'type': InterfaceTypeChoices.TYPE_OTHER},
)

print(f'Demo device: {device} (id={device.pk})')
print(f'Input interface: {input_interface} (id={input_interface.pk}) -> {input_interface.get_absolute_url()}')
print(f'Output interface: {output_interface} (id={output_interface.pk}) -> {output_interface.get_absolute_url()}')
