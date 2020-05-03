import JLinkHdlr
import IOCParser
import GPIOSampling

jlink = JLinkHdlr.jlink('STM32L053C8')

ioc = IOCParser.parseFile('../target/test_gpio_output/test_gpio_output.ioc')

#modify_register('RCC', 'IOPENR', 0b1, 1)
#gpio_setmode('GPIOA', 5, 1)
#gpio_setoutput('GPIOA', 5, 1)

dummy_read_for_caching = jlink.read_register('GPIOA', 'ODR')
dummy_read_for_caching = jlink.read_register('GPIOB', 'ODR')
dummy_read_for_caching = jlink.read_register('GPIOA', 'IDR')

GPIOSampling.plot_gpio(5, 0.01, ioc, jlink)