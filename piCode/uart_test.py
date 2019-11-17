from Helmholtz import HelmholtzCage
from uart_hasselhof import UartHasselhof

if __name__ == "__main__":

    L = 0.8
    d = 0.8 * 0.5445
    N = 23
            
    # detect the operating system, if windows, replace forward slashes with backslashes
    # code will work for macOS, linux, and windows
    pathstr = "../TestData/ThinSat_MagField_Vector.csv"
    """if platform.system() == 'Windows':
        str = "..\TestData\ThinSat_MagField_Vector.csv"
     """                       
    cage = HelmholtzCage(pathstr, L, d, N)
                                                          
    currentX = cage.get_current_x()
    currentY = cage.get_current_y()
    currentZ = cage.get_current_z()
                                                                          
    uart = UartHasselhof()
                                                                                  
    time_to_run = 10    
    sorted_list = uart.sort_input_lists(time_to_run, currentX, currentY, currentZ)
    uart.output_to_MC(sorted_list)

