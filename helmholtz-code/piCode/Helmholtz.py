import csv
import math
from datetime import datetime

class HelmholtzCage:
    def __init__(self, filename, L, d, N):
        self.__current_x = []
        self.__current_y = []
        self.__current_z = []

        # DON'T FORGET THAT B IS IN mGAUSS
        self.__magfield = MagField(filename)
        # set length of side of coil
        self.L = L
        # set distance between coils
        self.d = d
        # set number of wraps of wire
        self.N = N
        # set the multiplicative constants to use in current formula
        mu = 1.2566370614 * 10**-6 # N/A^2 = kg*m/(A^2*s^2)
        gamma = d / L # ratio of distance between coils to length of coil side
        curr_const = \
            (math.pi / 4) \
            * (self.L / (mu * self.N)) \
            * (1 + gamma**2) \
            * math.sqrt(2 + gamma**2)

        # The equation needs tesla, so we do B*10^-7
        # to convert mG to T.
        # Result is current in Amperes.
        get_I = lambda B: curr_const * B * 10**-7

        for mag in self.__magfield.get_mag_x():
            self.__current_x.append(get_I(mag))

        for mag in self.__magfield.get_mag_y():
            self.__current_y.append(get_I(mag))

        for mag in self.__magfield.get_mag_z():
            self.__current_z.append(get_I(mag))

    def get_current_x(self):
        return self.__current_x

    def get_current_y(self):
        return self.__current_y

    def get_current_z(self):
        return self.__current_z

    def get_mag_x(self):
        return self.__magfield.get_mag_x()

    def get_mag_y(self):
        return self.__magfield.get_mag_y()

    def get_mag_z(self):
        return self.__magfield.get_mag_z()

    def get_time(self):
        return self.__magfield.get_time()

    def get_realtime(self):
        return self.__magfield.get_realtime()

    def get_magfield(self):
        return self.__magfield


class MagField:
    def __init__(self, fname):
        self.__realtime = []
        self.__time = []
        self.__mag_x = []
        self.__mag_y = []
        self.__mag_z = []
        # magfield intensity is stored in mGauss!!!
        # therefore, the csv file is expected to be in mGauss as well!!

        # populate the vectors with csv information
        with open(fname, 'r') as csvfile:
            magreader = csv.reader(csvfile)
            next(magreader)  # skip the first row
            prevrow = next(magreader)  # use this to skip the last row
            for row in magreader:
                dtitem = prevrow[0]  # YYYY-MM-DDTHH:MM:SS.ss
                self.__time.append(
                    datetime(
                        int(dtitem[:4]),  # YYYY
                        int(dtitem[5:7]),  # MM
                        int(dtitem[8:10]),  # DD
                        int(dtitem[11:13]),  # HH
                        int(dtitem[14:16]),  # mm
                        int(dtitem[17:19])  # ss
                    )
                )
                self.__mag_x.append(float(prevrow[1]))
                self.__mag_y.append(float(prevrow[2]))
                self.__mag_z.append(float(prevrow[3]))
                prevrow = row

    def get_mag_x(self):
        return self.__mag_x

    def get_mag_y(self):
        return self.__mag_y

    def get_mag_z(self):
        return self.__mag_z

    def get_time(self):
        return self.__time

    def get_realtime(self):
        return self.__realtime
