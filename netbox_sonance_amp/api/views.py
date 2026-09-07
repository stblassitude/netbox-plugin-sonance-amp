from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import AmpInputSettingsFilterSet, AmpOutputSettingsFilterSet
from ..models import AmpInputSettings, AmpOutputSettings
from .serializers import AmpInputSettingsSerializer, AmpOutputSettingsSerializer


class AmpInputSettingsViewSet(NetBoxModelViewSet):
    queryset = AmpInputSettings.objects.prefetch_related('interface', 'tags')
    serializer_class = AmpInputSettingsSerializer
    filterset_class = AmpInputSettingsFilterSet


class AmpOutputSettingsViewSet(NetBoxModelViewSet):
    queryset = AmpOutputSettings.objects.prefetch_related('interface', 'tags')
    serializer_class = AmpOutputSettingsSerializer
    filterset_class = AmpOutputSettingsFilterSet
