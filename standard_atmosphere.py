from math import exp, sqrt


class std_atmosphere:
    """
    1976 Standard Atmosphere:
    z: [m]
    Reference:
    http://www.dept.aoe.vt.edu/~mason/Mason_f/stdatm.f
    """

    def __init__(self, z):
        self.z = z                  # Flight altitude
        self.T, self.P = std_atmosphere.std_atmos_model(self)
        self.rho = std_atmosphere.density(self)

    def std_atmos_model(self):
        """1976 Standard Atmosphere model"""
        K = 34.163195          # Constant
        C1 = .001               # Factor: m to Km
        H = C1 * self.z / (1 + C1 * self.z / 6356.766)
        if H < 11:
            T = 288.15 - 6.5 * H
            P = (288.15 / T) ** (- K / 6.5)
        elif H < 20:
            T = 216.65
            P = 0.22336 * exp(- K * (H - 11) / 216.65)
        elif H < 32:
            T = 216.65 + (H - 20)
            P = 0.054032 * (216.65 / T) ** K
        elif H < 47:
            T = 228.65 + 2.8 * (H - 32)
            P = .0085666 * (228.65 / T) ** (K / 2.8)
        elif H < 51:
            T = 270.65
            P = .0010945 * exp(- K * (H - 47) / 270.65)

        elif H < 71:
            T = 270.65 - 2.8 * (H - 51)
            P = .00066063 * (270.65 / T) ** (- K / 2.8)
        elif H < 84.852:
            T = 214.65 - 2 * (H - 71)
            P = 3.9046e-5 * (214.65 / T) ** (- K / 2)
        else:
            error = 'z:{} [m] ouf of limits for S.A.'.format(self.z)
            raise Exception(error)
        return T, P

    def temperature(self):
        """Temperature at "z" altitude """
        Tsl = 288.15                 # Temp. sea level
        T_ratio = self.T / 288.15
        return Tsl * T_ratio

    def pressure(self):
        """Pressure at "z" altitude """
        Psl = 101325                 # Press. sea level
        return Psl * self.P

    def density(self):
        """Density at "z" altitude """
        Rsl = 1.225                  # Density sea level
        R_ratio = self.P / (self.T / 288.15)
        return Rsl * R_ratio

    def sound_speed(self):
        """Sound speed at "z" altitude """
        Asl = 340.294                # Sound speed sea level
        T_ratio = self.T / 288.15
        return Asl * sqrt(T_ratio)

    def dynamic_pressure(self, U):
        """
        Dynamic pressure at "z" altitude
        U: air speed [m/s]
        """
        return (self.rho * U ** 2) / 2

    def viscosity_dynamic(self):
        """Dynamic viscosity - Sutherland Equation"""
        BT = 1.458E-06              # Beta constant for viscosity eq.
        return BT * self.T ** 1.5 / (self.T + 110.4)

    def viscosity_kinematic(self):
        u = std_atmosphere.viscosity_dynamic(self)
        return u / self.rho

    def Reynolds(self, x, U):
        """Reynolds number
           U: air speed [m/s]
           x: reference length [m] (airfoil/wing chord)
        """
        u = std_atmosphere.viscosity_dynamic(self)
        return (self.rho * U * x) / u

    def Mach(self, U):
        A = std_atmosphere.sound_speed(self)
        return U / A