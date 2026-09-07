# Netbox Plugin for Sonance Amp Input and Output Parameters

This plugin models SonAmp input and output parameters as an extension to an "Other" Interface.

## Data Model

Configuration parameters for inputs and outputs are stored in two models: AmpInputSettings and AmpOutputSettings, which are tied to an Interface through a one-to-one foreign key relationship.

For AmpInputSettings, the following fields are managed:
* Level Trim dB: value of -6.0 to 6.0 in 0.5 steps

The Interface Label field is applied to the Input Name parameter. This name is also what is offered when choosing an Output Source below; if an input interface has no label set, its name is used instead.

For AmpOutputSettings, the following fields are managed:
* Output Setup 
    * Stereo/Mono: "stereo" or "mono"
    * DSP Preset: preset name (freeform string)
    * Output Group: choice of "A" to "H"
    * Bridge Mode: "on" or "off"
* Output Source
    * Output Source 1: choice of any other interface on the same device configured with input amp parameters, offered by that interface's label (or name, if it has no label)
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

## REST API

Both models are fully exposed through NetBox's REST API, under the plugin's base path:

| Endpoint | Methods | Description |
|----------|---------|--------------|
| `/api/plugins/sonance-amp/input-settings/` | GET, POST | List / create AmpInputSettings |
| `/api/plugins/sonance-amp/input-settings/<id>/` | GET, PUT, PATCH, DELETE | Retrieve / update / delete a single AmpInputSettings |
| `/api/plugins/sonance-amp/output-settings/` | GET, POST | List / create AmpOutputSettings |
| `/api/plugins/sonance-amp/output-settings/<id>/` | GET, PUT, PATCH, DELETE | Retrieve / update / delete a single AmpOutputSettings |

These follow standard NetBox REST API conventions: authenticate with `Authorization: Token <your-api-token>` (or an authenticated browser session), page results with `?limit=`/`?offset=`, request compact nested objects with `?brief=1`, and free-text search with `?q=` (matching interface/device name, and output group for outputs). Both endpoints also support filtering by `interface_id`; output settings additionally filter on `stereo_mono`, `dsp_preset`, `output_group`, `bridge_mode`, `mode_source_2`, and `mute`.

Related objects -- `interface`, and for output settings `output_source_1`/`output_source_2` -- are represented as nested objects on read, and accept either a primary key or a set of attributes uniquely identifying the interface on write. Choice fields (`stereo_mono`, `output_group`, `mode_source_2`) are represented as `{"value": ..., "label": ...}` objects on read, but take just the raw value on write.

Example: fetch the output settings for a specific interface

```
GET /api/plugins/sonance-amp/output-settings/?interface_id=9
Authorization: Token <your-api-token>
```

Nested interface objects are trimmed below to the relevant fields; the actual response also includes each interface's `device`, `cable`, `description`, etc.

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "url": "https://netbox.example.com/api/plugins/sonance-amp/output-settings/1/",
      "display": "Output amp parameters for Speaker 1L (Library E L)",
      "interface": {
        "id": 9,
        "url": "https://netbox.example.com/api/dcim/interfaces/9/",
        "display": "Speaker 1L (Library E L)",
        "name": "Speaker 1L"
      },
      "stereo_mono": {"value": "stereo", "label": "Stereo"},
      "dsp_preset": "Main",
      "output_group": {"value": "A", "label": "A"},
      "bridge_mode": false,
      "output_source_1": {
        "id": 1,
        "url": "https://netbox.example.com/api/dcim/interfaces/1/",
        "display": "In 1L (1 Library)",
        "name": "In 1L"
      },
      "output_source_2": {
        "id": 2,
        "url": "https://netbox.example.com/api/dcim/interfaces/2/",
        "display": "In 1R (1 Library)",
        "name": "In 1R"
      },
      "mode_source_2": {"value": "mix", "label": "Mix"},
      "output_volume": 0.0,
      "turn_on_volume": -40.0,
      "maximum_volume": 6.0,
      "gain_offset": 0.0,
      "mute": false,
      "tags": [],
      "custom_fields": {},
      "created": "2026-09-07T10:00:00Z",
      "last_updated": "2026-09-07T10:00:00Z"
    }
  ]
}
```

Example: create output settings for an interface, routed from two input interfaces by their primary keys

```
POST /api/plugins/sonance-amp/output-settings/
Authorization: Token <your-api-token>
Content-Type: application/json

{
  "interface": 9,
  "stereo_mono": "stereo",
  "output_source_1": 1,
  "output_source_2": 2,
  "mode_source_2": "mix"
}
```

The full interactive API schema is also available from any running instance at `/api/docs/`, and every endpoint is browsable directly (with a form for authenticated write access) by visiting its URL in a browser.

## Compatibility

| NetBox Version | Plugin Version |
|-----------------|----------------|
| 4.1 - 4.99      | 0.1.0          |

## Installation

Install the plugin into your NetBox virtual environment:

```bash
pip install netbox-plugin-sonance-amp
```

Enable it in your NetBox `configuration.py` (or `plugins.py`, if using [netbox-docker](https://github.com/netbox-community/netbox-docker)):

```python
PLUGINS = [
    "netbox_plugin_sonance_amp",
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

Once the `netbox` service reports healthy, log in at <http://localhost:8000/> with `admin` / `admin`. A demo device, `sonamp-1`, is created automatically with 8 input interfaces (`In 1L` through `In 4R`, each already configured with input amp parameters) and 8 output interfaces (`Speaker 1L` through `Speaker 4R`, all type "Other") so you can open any interface's detail page and add amp parameters right away -- including picking an Output Source from the labeled inputs.

To stop and remove the stack (including its database volume):

```bash
docker compose down -v
```

