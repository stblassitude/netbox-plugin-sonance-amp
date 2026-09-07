from utilities.choices import ChoiceSet


class AmpParameterTypeChoices(ChoiceSet):
    """
    Which amp parameter set, if any, is attached to a given interface.
    """
    NONE = 'none'
    INPUT = 'input'
    OUTPUT = 'output'

    CHOICES = [
        (NONE, 'No amp parameters', 'gray'),
        (INPUT, 'Input amp parameters', 'blue'),
        (OUTPUT, 'Output amp parameters', 'green'),
    ]


class StereoModeChoices(ChoiceSet):
    STEREO = 'stereo'
    MONO = 'mono'

    CHOICES = [
        (STEREO, 'Stereo', 'blue'),
        (MONO, 'Mono', 'purple'),
    ]


class OutputGroupChoices(ChoiceSet):
    CHOICES = [(letter, letter) for letter in 'ABCDEFGH']


class OutputSourceChoices(ChoiceSet):
    CHOICES = [
        (f'{number}{channel}', f'{number}{channel}')
        for number in range(1, 5)
        for channel in ('L', 'R')
    ]


class ModeSource2Choices(ChoiceSet):
    MUTE = 'mute'
    MIX = 'mix'
    OFF = 'off'

    CHOICES = [
        (MUTE, 'Mute', 'red'),
        (MIX, 'Mix', 'blue'),
        (OFF, 'Off', 'gray'),
    ]
