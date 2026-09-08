from django.urls import path

from netbox.views.generic import ObjectChangeLogView

from . import views
from .models import AmpInputSettings, AmpOutputSettings

app_name = 'netbox_plugin_sonance_amp'

urlpatterns = (
    # AmpInputSettings
    path('input-settings/', views.AmpInputSettingsListView.as_view(), name='ampinputsettings_list'),
    path('input-settings/add/', views.AmpInputSettingsEditView.as_view(), name='ampinputsettings_add'),
    path(
        'input-settings/edit/', views.AmpInputSettingsBulkEditView.as_view(),
        name='ampinputsettings_bulk_edit',
    ),
    path(
        'input-settings/delete/', views.AmpInputSettingsBulkDeleteView.as_view(),
        name='ampinputsettings_bulk_delete',
    ),
    path('input-settings/<int:pk>/', views.AmpInputSettingsView.as_view(), name='ampinputsettings'),
    path('input-settings/<int:pk>/edit/', views.AmpInputSettingsEditView.as_view(), name='ampinputsettings_edit'),
    path(
        'input-settings/<int:pk>/delete/', views.AmpInputSettingsDeleteView.as_view(),
        name='ampinputsettings_delete',
    ),
    path(
        'input-settings/<int:pk>/changelog/', ObjectChangeLogView.as_view(),
        name='ampinputsettings_changelog', kwargs={'model': AmpInputSettings},
    ),

    # AmpOutputSettings
    path('output-settings/', views.AmpOutputSettingsListView.as_view(), name='ampoutputsettings_list'),
    path('output-settings/add/', views.AmpOutputSettingsEditView.as_view(), name='ampoutputsettings_add'),
    path(
        'output-settings/edit/', views.AmpOutputSettingsBulkEditView.as_view(),
        name='ampoutputsettings_bulk_edit',
    ),
    path(
        'output-settings/delete/', views.AmpOutputSettingsBulkDeleteView.as_view(),
        name='ampoutputsettings_bulk_delete',
    ),
    path('output-settings/<int:pk>/', views.AmpOutputSettingsView.as_view(), name='ampoutputsettings'),
    path(
        'output-settings/<int:pk>/edit/', views.AmpOutputSettingsEditView.as_view(),
        name='ampoutputsettings_edit',
    ),
    path(
        'output-settings/<int:pk>/delete/', views.AmpOutputSettingsDeleteView.as_view(),
        name='ampoutputsettings_delete',
    ),
    path(
        'output-settings/<int:pk>/changelog/', ObjectChangeLogView.as_view(),
        name='ampoutputsettings_changelog', kwargs={'model': AmpOutputSettings},
    ),

    # Combined interface amp parameter editor
    path(
        'interfaces/<int:interface_id>/amp-parameters/edit/', views.InterfaceAmpParametersEditView.as_view(),
        name='interface_amp_parameters',
    ),
)
