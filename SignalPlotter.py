import time
import JLinkWrapper

import IOCParser

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Plotter:
    def __init__(self, ioc, jlink, elfreader):
        self._ioc = ioc
        self._jlink = jlink
        self._elfreader = elfreader

    def _read_gpio(self):
        gpio_data = dict()
        
        input_reg_data = dict()
        output_reg_data = dict()
        for i in self._ioc.inputGpios:
            input_reg_data[i] = self._jlink.read_register(i, 'IDR')
        for o in self._ioc.outputGpios:
            output_reg_data[o] = self._jlink.read_register(o, 'ODR')

        for sig in self._ioc.signals:
            if self._ioc.signals[sig] == 'GPIO_Input':
                gpio_data[sig] = (input_reg_data[self._ioc.gpio[sig]] >> self._ioc.pin_num[sig]) & 1
            if self._ioc.signals[sig] == 'GPIO_Output':
                gpio_data[sig] = (output_reg_data[self._ioc.gpio[sig]] >> self._ioc.pin_num[sig]) & 1

        return gpio_data


    def plot_gpio(self, time_sec, delta_sec):
        x_vals = []
        y_vals = [[] for i in range(len(self._ioc.signals))]

        start_time = time.time()

        while (time.time() - start_time) < time_sec:
            sample_time = time.time()
            x_vals.append(sample_time - start_time)
            data = self._read_gpio()
            idx = 0
            for val in data:
                y_vals[idx].append(data[val])
                idx += 1
            time_to_sleep = delta_sec - (time.time() - sample_time)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            else:
                print('Missed sample point by ' + str(time_to_sleep * -1) + ' seconds')

        # TODO: Create data in second thread and update once per second?
        _, ax = plt.subplots(len(self._ioc.digital_signals), sharex=True)
        
        if len(self._ioc.digital_signals) > 1:
            io_num = 0
            for sig in self._ioc.digital_signals:
                ax[io_num].cla()
                ax[io_num].set_title(sig + ' (' + self._ioc.labels[sig] + ') [' + self._ioc.signals[sig] + ']')
                ax[io_num].set_ylim([-0.2, 1.2])
                ax[io_num].set_yticks([0,1])
                ax[io_num].step(x_vals, y_vals[io_num])
                io_num += 1
        else:
            sig = next(iter(self._ioc.digital_signals.keys()))
            ax.cla()
            ax.set_title(sig + ' (' + self._ioc.labels[sig] + ') [' + self._ioc.signals[sig] + ']')
            ax.set_ylim([-0.2, 1.2])
            ax.set_yticks([0,1])
            ax.step(x_vals, y_vals[0])
        
        plt.subplots_adjust(hspace=1)
        plt.xlabel('time (sec)')
        plt.show()

    def plot_adc(self, time_sec, delta_sec):
        addr = self._elfreader.getAddressOfSym('adcBuffer')
        size = self._elfreader.getSizeOfSym('adcBuffer')
        num_elem = int(size / 2)
        
        x_vals = []
        y_vals = [[] for i in range(num_elem)]

        start_time = time.time()

        while (time.time() - start_time) < time_sec:
            sample_time = time.time()
            x_vals.append(sample_time - start_time)
            data = self._jlink.memory_read16(addr, num_elem)
            idx = 0
            for val in data:
                y_vals[idx].append(val)
                idx += 1
            time_to_sleep = delta_sec - (time.time() - sample_time)
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            else:
                print('Missed sample point by ' + str(time_to_sleep * -1) + ' seconds')

        # TODO: Create data in second thread and update once per second?
        _, ax = plt.subplots(num_elem, sharex=True)
            
        if num_elem > 1:
            io_num = 0
            # first print all signals of first ADC, then go to the next and so on...
            for adc in self._ioc.adcs:
                for sig in self._ioc.adcs[adc].regularConversionPins:
                    ax[io_num].cla()
                    ax[io_num].set_title(self._gen_adc_title(sig))
                    ax[io_num].plot(x_vals, y_vals[io_num])
                    io_num += 1
        else:
            # Print single signal
            sig = next(iter(self._ioc.analog_signals.keys()))
            ax.cla()
            ax.set_title(self._gen_adc_title(sig))
            ax.plot(x_vals, y_vals[0])
         
        plt.subplots_adjust(hspace=1)
        plt.xlabel('time (sec)')
        plt.show()
    
    def _gen_adc_title(self, sig):
        titlestr = sig
        if sig in self._ioc.labels:
            titlestr += ' (' + self._ioc.labels[sig] + ')'
        if sig in self._ioc.signals:
            titlestr += ' [' + self._ioc.signals[sig] + ']'
        return titlestr

    #def animate_gpio_plot(i, jlink):	
#	odr_val = jlink.read_register('GPIOA', 'ODR')
#	
#	x_vals.append(i)
#	
#	io_num = 0
#
#	for p in ax:
#		y_vals[io_num].append((odr_val >> io_num) & 1)
#		p.cla()
#		p.set_title('Bit ' + str(io_num))
#		p.step(x_vals, y_vals[io_num])
#		io_num += 1
#	
#	#for row in ax:
#	#	row.scatter(i, (odr_val >> pin) & 1)
#	#	pin += 1
#	plt.tight_layout()

#def plot_gpio(time, delta):
#	global ax
#	global y_vals
#
#	# TODO: Create data in second thread and update once per second?
#	fig,ax = plt.subplots(8)
#
#	for i in range(8):
#		y_vals.append([])
#
#	ani = FuncAnimation(plt.gcf(), animate_gpio_plot, interval=delta)
#
#	plt.tight_layout()
#	plt.show()

#def plot_gpio(time, delta):
#   fig, ax = plt.subplots(8, sharex=True)
#   fig.suptitle('Bla')
#   for i in range(time):
#       odr_val = read_register('GPIOA', 'ODR')
#       pin = 0
#       for row in ax:
#           row.scatter(i, (odr_val >> pin) & 1)
#           pin += 1
#       plt.pause(0.05)
#