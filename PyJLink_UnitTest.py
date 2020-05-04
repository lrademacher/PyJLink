import JLinkWrapper
import IOCParser
import ELFRead

jlink = JLinkWrapper.JLink('STM32L053C8')
ioc = IOCParser.parseFile('../target/test_gpio_output/test_gpio_output.ioc')
elfreader = ELFRead.reader('D:\\Projects\\WILO\\Python_JLink\\target\\test_gpio_output\\Debug\\test_gpio_output.elf')

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    
class TestGPIO(unittest.TestCase):
    def setUp(self):
        jlink.modify_register('RCC', 'IOPENR', 0b100, 0b100)

    def test_odr(self):
        jlink.modify_register('GPIOC', 'ODR', 0xff, 0xcd)
        self.assertEqual(jlink.read_register('GPIOC', 'ODR') & 0xff, 0xcd)

if __name__ == '__main__':
    unittest.main()
