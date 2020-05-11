import time
import JLinkWrapper

import IOCParser

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ax = []
x_vals = []
y_vals = []

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

def read_gpio(ioc, jlink):
    gpio_data = dict()
    
    input_reg_data = dict()
    output_reg_data = dict()
    for i in ioc.inputGpios:
        input_reg_data[i] = jlink.read_register(i, 'IDR')
    for o in ioc.outputGpios:
        output_reg_data[o] = jlink.read_register(o, 'ODR')

    for sig in ioc.signals:
        if ioc.signals[sig] == 'GPIO_Input':
            gpio_data[sig] = (input_reg_data[ioc.gpio[sig]] >> ioc.pin_num[sig]) & 1
        if ioc.signals[sig] == 'GPIO_Output':
            gpio_data[sig] = (output_reg_data[ioc.gpio[sig]] >> ioc.pin_num[sig]) & 1

    return gpio_data


def plot_gpio(time_sec, delta_sec, ioc, jlink):
    x_vals = []
    y_vals = [[] for i in range(len(ioc.signals))]

    start_time = time.time()

    while (time.time() - start_time) < time_sec:
        sample_time = time.time()
        x_vals.append(sample_time - start_time)
        data = read_gpio(ioc, jlink)
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
    _, ax = plt.subplots(len(ioc.digital_signals), sharex=True)
    
    if len(ioc.digital_signals) > 1:
      io_num = 0
      for sig in ioc.digital_signals:
          ax[io_num].cla()
          ax[io_num].set_title(sig + ' (' + ioc.labels[sig] + ') [' + ioc.signals[sig] + ']')
          ax[io_num].set_ylim([-0.2, 1.2])
          ax[io_num].set_yticks([0,1])
          ax[io_num].step(x_vals, y_vals[io_num])
          io_num += 1
    else:
      sig = next(iter(ioc.digital_signals.keys()))
      ax.cla()
      ax.set_title(sig + ' (' + ioc.labels[sig] + ') [' + ioc.signals[sig] + ']')
      ax.set_ylim([-0.2, 1.2])
      ax.set_yticks([0,1])
      ax.step(x_vals, y_vals[0])
    
    plt.subplots_adjust(hspace=1)
    plt.xlabel('time (sec)')
    plt.show()

def plot_adc(time_sec, delta_sec, addr, size, ioc, jlink):
    num_elem = int(size / 2)
    x_vals = []
    y_vals = [[] for i in range(num_elem)]

    start_time = time.time()

    while (time.time() - start_time) < time_sec:
        sample_time = time.time()
        x_vals.append(sample_time - start_time)
        data = jlink.memory_read16(addr, num_elem)
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
      for sig in ioc.analog_signals:
          ax[io_num].cla()
          ax[io_num].set_title(sig + ' (' + ioc.labels[sig] + ') [' + ioc.signals[sig] + ']')
          ax[io_num].plot(x_vals, y_vals[io_num])
          io_num += 1
    else:
      sig = next(iter(ioc.analog_signals.keys()))
      ax.cla()
      ax.set_title(sig + ' (' + ioc.labels[sig] + ') [' + ioc.signals[sig] + ']')
      ax.plot(x_vals, y_vals[0])
        
    plt.subplots_adjust(hspace=1)
    plt.xlabel('time (sec)')
    plt.show()