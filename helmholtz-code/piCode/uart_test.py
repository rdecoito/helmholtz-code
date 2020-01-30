from Helmholtz import HelmholtzCage
from uart_hasselhof import UartHasselhof
import os
import time

if __name__ == "__main__":
    L = 0.8
    d = 0.8 * 0.5445
    N = 23

    # detect the operating system, if windows, replace forward slashes with backslashes
    # code will work for macOS, linux, and windows
    pathstr = str(os.path.join("..", "TestData", "ThinSat_MagField_Vector.csv"))

    t = time.time()
    cage = HelmholtzCage(pathstr, L, d, N)
    t2 = time.time()
    print(f'Setup time: {float(t2 - t)}')

    currentX = cage.get_current_x()
    currentY = cage.get_current_y()
    currentZ = cage.get_current_z()

    uart = UartHasselhof()

    time_to_run = 10
    baudrate = 9600

    t = time.time()
    sorted_list = uart.sort_input_lists(time_to_run, currentX, currentY, currentZ)
    t2 = time.time()
    print(f'Pre-processing time: {float(t2 - t)}')

    t = time.time_ns()
    uart.output_to_MC(sorted_list, baudrate)
    t2 = time.time_ns()
    print(f'Transmit time: {float(t2-t)/(10**9)}')

