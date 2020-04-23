import standard_atmosphere as std


# Initialize an object
flight = std.std_atmosphere(2850)     # One input: z - altitude

# Density
print('Altitude {} [m]'.format(flight.z))
print(flight.temperature())
print(flight.pressure())
print(flight.density())
print(flight.sound_speed())
print(flight.dynamic_pressure(10))    # One input: air speed
print(flight.viscosity_dynamic())
print(flight.viscosity_kinematic())
print(flight.Reynolds(0.305, 10))     # two inputs: ref. length and air speed
print(flight.Mach(50))                # One input: air speed

# Perform multipoint analysis
Z = [0, 1500, 3000, 4500, 10000]      # list of flight altitudes

# Density value for various flight altitudes
densities = [std.std_atmosphere(z).density() for z in Z]

# Mach number for various flight speeds at a fixed flight altitude
# range of flight speeds range from 10 to 50 with steps of 5
Mach_numbers = [std.std_atmosphere(1500).Mach(u) for u in range(10, 50, 5)]

# Reynolds number at differente flight speeds and altitudes

Z = [0, 1500, 3000, 4500, 10000]     # For each z, there is a flight speed
U = [30, 35, 40, 45, 50]

Reynolds_numbers = [std.std_atmosphere(z).Reynolds(0.2, U[x])
                    for x, z in enumerate(Z)]
