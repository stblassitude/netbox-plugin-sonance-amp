from netbox.api.routers import NetBoxRouter

from . import views

app_name = 'netbox_sonance_amp'

router = NetBoxRouter()
router.register('input-settings', views.AmpInputSettingsViewSet)
router.register('output-settings', views.AmpOutputSettingsViewSet)

urlpatterns = router.urls
