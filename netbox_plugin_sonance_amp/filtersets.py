from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from .models import AmpInputSettings, AmpOutputSettings


class AmpInputSettingsFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = AmpInputSettings
        fields = ('id', 'interface', 'level_trim_db')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(interface__name__icontains=value) |
            Q(interface__device__name__icontains=value)
        )


class AmpOutputSettingsFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = AmpOutputSettings
        fields = (
            'id', 'interface', 'stereo_mono', 'dsp_preset', 'output_group', 'bridge_mode', 'mode_source_2', 'mute',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(interface__name__icontains=value) |
            Q(interface__device__name__icontains=value) |
            Q(output_group__icontains=value)
        )
