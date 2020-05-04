import JLinkHdlr
import IOCParser
import SignalPlotter
import ELFRead

jlink = JLinkHdlr.jlink('STM32L053C8')
ioc = IOCParser.parseFile('../target/test_gpio_output/test_gpio_output.ioc')
elfreader = ELFRead.reader('D:\\Projects\\WILO\\Python_JLink\\target\\test_gpio_output\\Debug\\test_gpio_output.elf')

#modify_register('RCC', 'IOPENR', 0b1, 1)
#gpio_setmode('GPIOA', 5, 1)
#gpio_setoutput('GPIOA', 5, 1)

# SignalPlotter.plot_gpio(5, 0.01, ioc, jlink)
#SignalPlotter.plot_adc(5, 0.01, elfreader.getAddressOfSym('adcBuffer'), elfreader.getSizeOfSym('adcBuffer'), ioc, jlink)

