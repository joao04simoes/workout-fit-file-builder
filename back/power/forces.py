import math
from power.wind import WindSpeedAndDir, wind
import pandas as pd


def CalculateSlope(dataPoint, nPoints,):
    for i in range(0, nPoints-1):
        if (dataPoint[i+1].altitude - dataPoint[i].altitude) != 0 and dataPoint[i+1].distance - dataPoint[i].distance != 0:
            slope = ((dataPoint[i+1].altitude - dataPoint[i].altitude) /
                     (dataPoint[i+1].distance - dataPoint[i].distance))
            if abs(slope) < 0.30:
                dataPoint[i].slope = math.atan(slope)
        else:
            # if (dataPoint[i].distance > 24519 and dataPoint[i].distance < 24720):
            # print("distance", dataPoint[i].distance)
            # print("distance next", dataPoint[i+1].distance)
            # print("altitude", dataPoint[i].altitude)
            # print("altitude next", dataPoint[i+1].altitude)
            # print("before slope", dataPoint[i-1].slope)
            # print("---------------------")

            dataPoint[i].slope = 0


def PotenciaGravidade(dataPoint, nPoints, bikeConstants):
    max = 0
    for i in range(0, nPoints-1):
        force = bikeConstants.weight * \
            bikeConstants.G * math.sin(dataPoint[i].slope)
        dataPoint[i].powerGravity = force * dataPoint[i].speed
        if dataPoint[i].powerGravity > max:
            max = dataPoint[i].powerGravity
    return max


def calculateWindFavor(dataPoint, roundedlist):
    timestamp = pd.Timestamp(dataPoint[0].time,)
    rounded_timestamp = timestamp - \
        pd.Timedelta(minutes=timestamp.minute %
                     15, seconds=timestamp.second, microseconds=timestamp.microsecond)

    minutely_15_dataframe = wind(
        rounded_timestamp, roundedlist)

    wFavor = []

    for i in range(0, len(dataPoint)-1):
        (windDir, windSpeed) = WindSpeedAndDir(
            dataPoint, i, minutely_15_dataframe)
        wFavor.append(windFavor(dataPoint, windDir, windSpeed, i))

    return wFavor


def PowerResistenceAir(dataPoint, nPoints, bikeConstants, windFavor):

    max = 0
    soma = 0

    for i in range(0, nPoints-1):

        force = 0.5 * bikeConstants.CdA * \
            bikeConstants.density * ((dataPoint[i].speed + windFavor[i]) ** 2)
        dataPoint[i].powerAir = force * dataPoint[i].speed
        if dataPoint[i].powerAir > max:
            max = dataPoint[i].powerAir
        soma = soma + dataPoint[i].powerAir

    return max


def PowerRollingRestiance(dataPoint, nPoints, bikeConstants):
    for i in range(0, nPoints-1):
        force = bikeConstants.weight * bikeConstants.G * \
            math.cos(dataPoint[i].slope)*bikeConstants.Crr
        dataPoint[i].powerRR = force*dataPoint[i].speed


def windFavor(dataPoint, windDir, windSpeed, i):
    lat1, lon1, lat2, lon2 = map(math.radians, [
                                 dataPoint[i].lat, dataPoint[i].long, dataPoint[i+1].lat, dataPoint[i+1].long])
    # Difference in longitudes
    delta_lon = lon2 - lon1
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(delta_lon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    # print("windspeed", windSpeed)
    windSpeed = windSpeed * math.cos(math.radians(compass_bearing - windDir))

    # print("bearing", compass_bearing)
    # print("windDir", windDir)
    # print("diference", compass_bearing - windDir)
    # print("real wind ", windSpeed)
    return windSpeed
