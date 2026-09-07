from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

input_settings_buttons = (
    PluginMenuButton(
        link='plugins:netbox_sonance_amp:ampinputsettings_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
)

output_settings_buttons = (
    PluginMenuButton(
        link='plugins:netbox_sonance_amp:ampoutputsettings_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN,
    ),
)

menu = PluginMenu(
    label='Sonance Amp',
    icon_class='mdi mdi-volume-high',
    groups=(
        ('Amp Parameters', (
            PluginMenuItem(
                link='plugins:netbox_sonance_amp:ampinputsettings_list',
                link_text='Input Settings',
                buttons=input_settings_buttons,
            ),
            PluginMenuItem(
                link='plugins:netbox_sonance_amp:ampoutputsettings_list',
                link_text='Output Settings',
                buttons=output_settings_buttons,
            ),
        )),
    ),
)
