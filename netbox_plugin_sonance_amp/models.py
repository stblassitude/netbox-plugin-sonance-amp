from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel

from .choices import ModeSource2Choices, OutputGroupChoices, OutputSourceChoices, StereoModeChoices


class AmpInputSettings(NetBoxModel):
    """
    SonAmp input parameters for an interface configured as an amplifier input.
    """
    interface = models.OneToOneField(
        to='dcim.Interface',
        on_delete=models.CASCADE,
        related_name='sonance_amp_input_settings',
    )
    level_trim_db = models.DecimalField(
        verbose_name='level trim (dB)',
        max_digits=4,
        decimal_places=1,
        default=0,
        validators=(MinValueValidator(-18), MaxValueValidator(18)),
    )

    class Meta:
        ordering = ('interface',)
        verbose_name = 'amp input settings'
        verbose_name_plural = 'amp input settings'

    def __str__(self):
        return f'Input amp parameters for {self.interface}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_plugin_sonance_amp:ampinputsettings', args=[self.pk])


class AmpOutputSettings(NetBoxModel):
    """
    SonAmp output parameters for an interface configured as an amplifier output.
    """
    interface = models.OneToOneField(
        to='dcim.Interface',
        on_delete=models.CASCADE,
        related_name='sonance_amp_output_settings',
    )

    # Output Setup
    stereo_mono = models.CharField(
        verbose_name='stereo/mono',
        max_length=10,
        choices=StereoModeChoices,
        default=StereoModeChoices.STEREO,
    )
    dsp_preset = models.CharField(
        verbose_name='DSP preset',
        max_length=100,
        blank=True,
    )
    output_group = models.CharField(
        verbose_name='output group',
        max_length=1,
        choices=OutputGroupChoices,
        blank=True,
    )
    bridge_mode = models.BooleanField(
        verbose_name='bridge mode',
        default=False,
    )

    # Output Source
    output_source_1 = models.CharField(
        verbose_name='output source 1',
        max_length=2,
        choices=OutputSourceChoices,
        blank=True,
    )
    output_source_2 = models.CharField(
        verbose_name='output source 2',
        max_length=2,
        choices=OutputSourceChoices,
        blank=True,
    )
    mode_source_2 = models.CharField(
        verbose_name='mode source 2',
        max_length=10,
        choices=ModeSource2Choices,
        default=ModeSource2Choices.OFF,
        blank=True,
    )

    # Output Volume
    output_volume = models.DecimalField(
        verbose_name='output volume (dB)',
        max_digits=4,
        decimal_places=1,
        default=0,
        validators=(MinValueValidator(-70), MaxValueValidator(12)),
    )
    turn_on_volume = models.DecimalField(
        verbose_name='turn-on volume (dB)',
        max_digits=4,
        decimal_places=1,
        default=-70,
        validators=(MinValueValidator(-70), MaxValueValidator(12)),
    )
    maximum_volume = models.DecimalField(
        verbose_name='maximum volume (dB)',
        max_digits=4,
        decimal_places=1,
        default=12,
        validators=(MinValueValidator(-70), MaxValueValidator(12)),
    )
    gain_offset = models.DecimalField(
        verbose_name='gain offset (dB)',
        max_digits=3,
        decimal_places=1,
        default=0,
        validators=(MinValueValidator(-6), MaxValueValidator(6)),
    )
    mute = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ('interface',)
        verbose_name = 'amp output settings'
        verbose_name_plural = 'amp output settings'

    def __str__(self):
        return f'Output amp parameters for {self.interface}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_plugin_sonance_amp:ampoutputsettings', args=[self.pk])
