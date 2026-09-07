from netbox.plugins import PluginConfig


class SonanceAmpConfig(PluginConfig):
    name = 'netbox_sonance_amp'
    verbose_name = 'Sonance Amp'
    description = 'Model Sonance SonAmp input and output parameters on NetBox interfaces'
    version = '0.1.0'
    author = 'Stefan Bethke'
    author_email = 'stb@lassitu.de'
    base_url = 'sonance-amp'
    min_version = '4.1.0'
    max_version = '4.99.99'
    default_settings = {}


config = SonanceAmpConfig
