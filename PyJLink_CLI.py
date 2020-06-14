import JLinkWrapper
import IOCParser
import SignalPlotter
import ELFRead

#jlink = JLinkWrapper.JLink('STM32L053C8')
jlink = JLinkWrapper.JLink('STM32F446RE')

#ioc = IOCParser.IOC('../target/test_gpio_output/test_gpio_output.ioc')
ioc = IOCParser.IOC('../target/test_f4/test_f4.ioc')

#elfreader = ELFRead.reader('D:\\Projects\\WILO\\Python_JLink\\target\\test_gpio_output\\Debug\\test_gpio_output.elf')
elfreader = ELFRead.reader('D:\\Projects\\WILO\\Python_JLink\\target\\test_f4\\Debug\\test_f4.elf')

plot = SignalPlotter.Plotter(ioc, jlink, elfreader)

#modify_register('RCC', 'IOPENR', 0b1, 1)
#gpio_setmode('GPIOA', 5, 1)
#gpio_setoutput('GPIOA', 5, 1)

#plot.plot_gpio(5, 0.01)
plot.plot_adc(5, 0.01)
