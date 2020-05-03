import re
pattern_gpio_signal = re.compile("^(P[A-Z][0-9]+).Signal=(.*)$")
pattern_gpio_label = re.compile("^(P[A-Z][0-9]+).GPIO_Label=(.*)$")
pattern_gpio_name_split = re.compile("^P([A-Z])([0-9]+)$")

class IOC:
  labels = dict()
  signals = dict()
  gpio = dict()
  pin_num = dict()
  inputGpios = []
  outputGpios = []

def parseFile(filename):
    ioc = IOC()
    for i, line in enumerate(open(filename)):
        for match in re.finditer(pattern_gpio_signal, line):
            ioc.signals[match.groups()[0]] = match.groups()[1]
            name_split_match = re.findall(pattern_gpio_name_split, match.groups()[0])
            if len(name_split_match) == 1:
                ioc.gpio[match.groups()[0]] = 'GPIO' + name_split_match[0][0]
                ioc.pin_num[match.groups()[0]] = int(name_split_match[0][1])
        for match in re.finditer(pattern_gpio_label, line):
            ioc.labels[match.groups()[0]] = match.groups()[1]
    setInputOutputGpio(ioc)
    return ioc

def setInputOutputGpio(ioc):
    for pin in ioc.gpio:
        if ioc.signals[pin] == 'GPIO_Input' and not ioc.gpio[pin] in ioc.inputGpios:
            ioc.inputGpios.append(ioc.gpio[pin])
        if ioc.signals[pin] == 'GPIO_Output' and not ioc.gpio[pin] in ioc.outputGpios:
            ioc.outputGpios.append(ioc.gpio[pin])