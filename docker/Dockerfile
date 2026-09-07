# Builds a NetBox image with this plugin installed, for local testing via docker-compose.yml
# at the root of the repository.
ARG NETBOX_IMAGE=netboxcommunity/netbox:v4.7

FROM ${NETBOX_IMAGE}

COPY . /source/netbox-plugin-sonance-amp
RUN /usr/local/bin/uv pip install --no-cache /source/netbox-plugin-sonance-amp \
    && rm -rf /source/netbox-plugin-sonance-amp

COPY docker/plugins.py /etc/netbox/config/plugins.py

RUN SECRET_KEY="dummydummydummydummydummydummydummydummydummydummy" \
    python /opt/netbox/netbox/manage.py collectstatic --no-input --no-color
