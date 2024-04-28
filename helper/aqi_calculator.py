#calculate aqi index for pm 2.5

def calculate_aqi_pm25(pm25):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (250, 500, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= pm25 <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (pm25 - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


#calculate aqi index for pm 10

def calculate_aqi_pm10(pm10):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (430, 500, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= pm10 <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (pm10 - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


#calculate aqi index for no2

def calculate_aqi_no2(no2):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (400, 500, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= no2 <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (no2 - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


#calculate aqi index for nh3

def calculate_aqi_nh3(nh3):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 200, 0, 50),
        (201, 400, 51, 100),
        (401, 800, 101, 200),
        (801, 1200, 201, 300),
        (1201, 1800, 301, 400),
        (1801, 2000, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= nh3 <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (nh3 - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


#calculate aqi index for so2

def calculate_aqi_so2(so2):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, 2000, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= so2 <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (so2 - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


#calculate aqi index for co

def calculate_aqi_co(co):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 1.0, 0, 50),
        (1.1, 2.0, 51, 100),
        (2.1, 10, 101, 200),
        (10.1, 17, 201, 300),
        (17.1, 34, 301, 400),
        (34, 50, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= co <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (co - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


#calculate aqi index for ozone

def calculate_aqi_ozone(ozone):
    # Define the AQI breakpoint ranges and corresponding AQI values for PM2.5
    breakpoints = [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 168, 101, 200),
        (169, 208, 201, 300),
        (209, 748, 301, 400),
        (748, 1000, 401, 500),
    ]

    # Find the range where the PM2.5 concentration falls
    for bp in breakpoints:
        if bp[0] <= ozone <= bp[1]:
            c_low, c_high, aqi_low, aqi_high = bp
            # Calculate AQI based on the formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (ozone - c_low) + aqi_low
            return round(aqi)

    return 500  # If the value exceeds the highest range, return the maximum AQI value (500)


def calculate_AQI(pollutants):
    aqi_dict = {}
#   for i in range(lenpollutants):
    aqi_pm25 = calculate_aqi_pm25(pollutants[0])
    aqi_pm10 = calculate_aqi_pm10(pollutants[1])
    aqi_no2 = calculate_aqi_no2(pollutants[2])
    aqi_nh3 = calculate_aqi_nh3(pollutants[3])
    aqi_so2 = calculate_aqi_so2(pollutants[4])
    aqi_co = calculate_aqi_co(pollutants[5])
    aqi_ozone = calculate_aqi_ozone(pollutants[6])

    aqi = max(aqi_pm25, aqi_pm10, aqi_no2, aqi_nh3, aqi_so2, aqi_co, aqi_ozone)

    return aqi


# aqi = calculate_AQI([150.63,	215.19,	22.98,	26.84,	2.77,	0.93,	56.35])
# print('17 hrs (5pm): ',aqi)

# aqi = calculate_AQI([438.24,	626.05,	22.76,	26.96,	2.74,	0.92,	56.37])
# print('18 hrs (6pm): ',aqi)


