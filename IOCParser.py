import re

class Adc:
    def __init__(self):
        self.regularConversionChannels = []
        self.regularConversionPins = []

class IOC:
    _pattern_gpio_signal = re.compile(r"^(P[A-Z][0-9]+).*\.Signal=(.*)$")
    _pattern_gpio_label = re.compile(r"^(P[A-Z][0-9]+)\.GPIO_Label=(.*)$")
    _pattern_gpio_name_split = re.compile("^P([A-Z])([0-9]+)$")
    _pattern_adc_channel_regular_conv = re.compile(r"^(ADC[0-9]+)\.Channel-[0-9]+\\#ChannelRegularConversion=ADC_CHANNEL_([0-9]+)$")
    _pattern_extract_adc_channel = re.compile("^ADC_IN([0-9]+)$")

    def __init__(self, filename):
        self.signals = dict()
        self.digital_signals = dict()
        self.analog_signals = dict()
        self.adcs = dict()
        self.labels = dict()
        self.gpio = dict()
        self.pin_num = dict()
        self.inputGpios = []
        self.outputGpios = []
        for _, line in enumerate(open(filename)):
            self._matchGpioRegex(line)
            self._matchAdcRegex(line)
        self._setInputOutputGpio()
        self.digital_signals = dict(filter(lambda elem: elem[1] == 'GPIO_Output' or elem[1] == 'GPIO_Input', self.signals.items()))
        self.analog_signals = dict(filter(lambda elem: elem[1].startswith('ADC'), self.signals.items()))
        if 'ADC' in self.adcs:
            self._extractSimpleAdcSetup()
        self._convertConversionChannelsToPins()

    def _matchGpioRegex(self, line):
        for match in re.finditer(self._pattern_gpio_signal, line):
            self.signals[match.groups()[0]] = match.groups()[1]
            name_split_match = re.findall(self._pattern_gpio_name_split, match.groups()[0])
            if len(name_split_match) == 1:
                self.gpio[match.groups()[0]] = 'GPIO' + name_split_match[0][0]
                self.pin_num[match.groups()[0]] = int(name_split_match[0][1])
        for match in re.finditer(self._pattern_gpio_label, line):
            self.labels[match.groups()[0]] = match.groups()[1]

    def _matchAdcRegex(self, line):
        for match in re.finditer(self._pattern_adc_channel_regular_conv, line):
            if not match.groups()[0] in self.adcs:
                self.adcs[match.groups()[0]] = Adc()
            self.adcs[match.groups()[0]].regularConversionChannels.append(int(match.groups()[1]))
        # simple case: Only one ADC:
        if line.startswith('ADC.IPParameters='):
            self.adcs['ADC'] = Adc()

    def _mapAdcChannelToPin(self, channel):
        for pin, analog_signal in self.analog_signals.items():
            if analog_signal.endswith('IN'+str(channel)):
                return pin
        return ''

    def _extractSimpleAdcSetup(self):
        for _, adc_channel in self.analog_signals.items():
            ch = re.findall(self._pattern_extract_adc_channel, adc_channel)[0]
            self.adcs['ADC'].regularConversionChannels.append(int(ch))

    def _convertConversionChannelsToPins(self):
        for _, adc in self.adcs.items():
            for channel in adc.regularConversionChannels:
                adc.regularConversionPins.append(self._mapAdcChannelToPin(channel))

    def _setInputOutputGpio(self):
        for pin in self.gpio:
            if self.signals[pin] == 'GPIO_Input' and not self.gpio[pin] in self.inputGpios:
                self.inputGpios.append(self.gpio[pin])
            if self.signals[pin] == 'GPIO_Output' and not self.gpio[pin] in self.outputGpios:
                self.outputGpios.append(self.gpio[pin])


# F0:
# PB1.Signal=ADC_IN9

# F4:
# ADC1.Channel-0\#ChannelRegularConversion=ADC_CHANNEL_0 => ADC1 => 1st conv = CH0
# PA0-WKUP.Signal=ADCx_IN0 => PA0 ADC_CH0

