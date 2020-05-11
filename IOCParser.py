import re

class IOC:
    _pattern_gpio_signal = re.compile("^(P[A-Z][0-9]+).Signal=(.*)$")
    _pattern_gpio_label = re.compile("^(P[A-Z][0-9]+).GPIO_Label=(.*)$")
    _pattern_gpio_name_split = re.compile("^P([A-Z])([0-9]+)$")

    def __init__(self, filename):
        self.signals = dict()
        self.digital_signals = dict()
        self.analog_signals = dict()
        self.labels = dict()
        self.gpio = dict()
        self.pin_num = dict()
        self.inputGpios = []
        self.outputGpios = []
        for _, line in enumerate(open(filename)):
            for match in re.finditer(self._pattern_gpio_signal, line):
                self.signals[match.groups()[0]] = match.groups()[1]
                name_split_match = re.findall(self._pattern_gpio_name_split, match.groups()[0])
                if len(name_split_match) == 1:
                    self.gpio[match.groups()[0]] = 'GPIO' + name_split_match[0][0]
                    self.pin_num[match.groups()[0]] = int(name_split_match[0][1])
            for match in re.finditer(self._pattern_gpio_label, line):
                self.labels[match.groups()[0]] = match.groups()[1]
        self._setInputOutputGpio()
        self.digital_signals = dict(filter(lambda elem: elem[1] == 'GPIO_Output' or elem[1] == 'GPIO_Input', self.signals.items()))
        # TODO: Sort analog signals as they will be sorted in analog value array
        self.analog_signals = dict(filter(lambda elem: elem[1].startswith('ADC'), self.signals.items()))


    def _setInputOutputGpio(self):
        for pin in self.gpio:
            if self.signals[pin] == 'GPIO_Input' and not self.gpio[pin] in self.inputGpios:
                self.inputGpios.append(self.gpio[pin])
            if self.signals[pin] == 'GPIO_Output' and not self.gpio[pin] in self.outputGpios:
                self.outputGpios.append(self.gpio[pin])