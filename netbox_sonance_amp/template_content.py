from netbox.plugins import PluginTemplateExtension


class InterfaceAmpParametersPanel(PluginTemplateExtension):
    models = ('dcim.interface',)

    def right_page(self):
        interface = self.context['object']
        return self.render('netbox_sonance_amp/inc/interface_panel.html', extra_context={
            'input_settings': getattr(interface, 'sonance_amp_input_settings', None),
            'output_settings': getattr(interface, 'sonance_amp_output_settings', None),
        })


template_extensions = (InterfaceAmpParametersPanel,)
