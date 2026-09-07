# Netbox Plugin for Sonance Amp Input and Output Parameters

This plugin models SonAmp input and output parameters as an extension to an "Other" Interface.

## Data Model

Configuration parameters for inputs and outputs are stored in two models: AmpInputSettings and AmpOutputSettings, which are tied to an Interface through a one-to-one foreign key relationship.

For AmpInputSettings, the following fields are managed:
* Level Trim dB: value of -6.0 to 6.0 in 0.5 steps

The Interface Label field is applied to the Input Name parameter.

For AmpOutputSettings, the following fields are managed:
* Output Setup 
    * Stereo/Mono: "stereo" or "mono"
    * DSP Preset: preset name (freeform string)
    * Output Group: choice of "A" to "H"
    * Bridge Mode: "on" or "off"
* Output Source
    * Output Source 1: choice of "1L", "1R", ... to "4R"
    * Output Source 2: as above
    * Mode Source 2: choice of "mute", "mix", or "off"
* Output Volume
    * Output Volume: value between -70 and 12
    * Turn On Volume: as above
    * Maximum Volume: as above
    * Gain Offset: value of -6.0 to 6.0 in 0.5 steps
    * Mute: "on" or "off"

The Interface Label field is applied to the Output Name parameter.

## User Interface

The plugin ties the custom model editing into the Interface detail form. The editing form allows choosing "No amp parameters", "Input amp parameters", or "Output amp parameters" for each interface. Changing the type will add or remove the respective model entry, and show the correct form for the type.

## Compatibility

| NetBox Version | Plugin Version |
|-----------------|----------------|
| 4.1 - 4.99      | 0.1.0          |

## Installation

Install the plugin into your NetBox virtual environment:

```bash
pip install netbox-sonance-amp
```

Enable it in your NetBox `configuration.py` (or `plugins.py`, if using [netbox-docker](https://github.com/netbox-community/netbox-docker)):

```python
PLUGINS = [
    "netbox_sonance_amp",
]
```

Then run migrations and restart NetBox:

```bash
python manage.py migrate
python manage.py collectstatic --no-input
```

## Development / Testing

A self-contained Docker Compose setup is included for trying the plugin out against a real NetBox instance. It builds a NetBox image with the plugin installed from this repository's source, so no packaging or PyPI publish is required.

```bash
docker compose up -d --build
```

Once the `netbox` service reports healthy, log in at <http://localhost:8000/> with `admin` / `admin`. A demo device, `sonamp-1`, is created automatically with an `Input 1` and an `Output 1` interface (both type "Other") so you can open either interface's detail page and add amp parameters right away.

To stop and remove the stack (including its database volume):

```bash
docker compose down -v
```

