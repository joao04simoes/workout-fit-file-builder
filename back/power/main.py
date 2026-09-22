import math
from power.forces import CalculateSlope, PotenciaGravidade, PowerResistenceAir, PowerRollingRestiance, calculateWindFavor
from fit_tool.fit_file import FitFile
import numpy as np
import power.segments as segments
from power.dataPoint import DataPoint
from power.utils import ReadFitFile as ReadFitFileData, derivative, ReadCsvFile
import json
import matplotlib.pyplot as plt


class BikeConstants:
    # btt dirt crr = 0.014 btt estrada = 0.005
    def __init__(self, G=9.81, weight=96, CdA=0.39, density=1.240088, Crr=0.005, losses=0.05):
        self.G = G
        self.weight = weight
        self.CdA = CdA
        self.density = density
        self.Crr = Crr
        self.losses = losses


def listCoordinates(dataPoints):
    roundedlist = list(
        {(round(item.lat, 2), round(item.long, 2)) for item in dataPoints})
    print(roundedlist)
    return roundedlist


def moving_average_np(values, window=10):
    values = np.array(values, dtype=float)
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="same")


def ReadFitFile(Filepath, isFitFile):
    dataPoints = []

    if (isFitFile):
        print("Reading FIT file...")
        fit_file = FitFile.from_file(Filepath)
        ReadFitFileData(fit_file, dataPoints)
    else:
        print("Reading CSV file...")
        ReadCsvFile(Filepath, dataPoints)

    if not dataPoints:
        print("No data points found.")
        return

    print("Data points read successfully.")

    return dataPoints


def calculatePower(dataPoints, nPoints, bikeConstants):

    RealPower = []
    PositivePower = []
    SampleDistance = []
    for i in range(0, nPoints-1):
        power = (dataPoints[i].powerGravity +
                 dataPoints[i].powerAir + dataPoints[i].powerRR) * (bikeConstants.losses + 1)

        if power > 0 and dataPoints[i].cadence > 20:

            power = round(power, 2)
            PositivePower.append(power)
            SampleDistance.append(dataPoints[i].distance)

            dataPoints[i].power = power
            RealPower.append(dataPoints[i].realPower)

    PositivePower = np.array(PositivePower)
    RealPower = np.array(RealPower)
    SampleDistance = np.array(SampleDistance)

    # grafico

    Figure = plt.figure(figsize=(10, 6))
    plt.plot(SampleDistance, PositivePower,
             label='Calculated Power', color='blue')
    plt.plot(SampleDistance, RealPower, label='Real Power', color='orange')
    plt.title('Calculated Power vs Real Power')
    plt.xlabel('Distance (m)')
    plt.ylabel('Power (Watts)')
    plt.legend()
    plt.grid()
    plt.show()

    media = PositivePower.sum()/len(PositivePower)
    mediaReal = RealPower.sum()/len(RealPower)

    return media, mediaReal


def toJson(dataPoints, nPoints):
    laps = segments.FindLaps(dataPoints, nPoints)
    derivative(dataPoints, nPoints)
    all_laps = []

    for lap in laps:
        n = dataPoints[lap.end].distance - dataPoints[lap.start].distance
        if n <= 0:
            n = 1.0

        speeds = [float(dataPoints[i].speed * 3.6)
                  for i in range(lap.start, lap.end + 1)]
        powers = [float(dataPoints[i].power)
                  for i in range(lap.start, lap.end + 1)]
        realPowers = [float(dataPoints[i].realPower)
                      for i in range(lap.start, lap.end + 1)]
        derivativeSpeeds = [float(dataPoints[i].derivativeSpeed * 3.6)
                            for i in range(lap.start, lap.end + 1)]
        derivativePowers = [float(dataPoints[i].derivativePower)
                            for i in range(lap.start, lap.end + 1)]

        smooth_speed = moving_average_np(speeds, window=5)
        smooth_power = moving_average_np(powers, window=5)
        smooth_real_power = moving_average_np(realPowers, window=7)
        smooth_derivative_speed = moving_average_np(derivativeSpeeds, window=5)
        smooth_derivative_power = moving_average_np(derivativePowers, window=5)

        points = []
        for idx, i in enumerate(range(lap.start, lap.end + 1)):
            points.append({
                "time": (dataPoints[i].distance - dataPoints[lap.start].distance) / (n) * 100,
                "speed": float(smooth_speed[idx]),
                "power": float(smooth_power[idx]),
                "realPower": float(smooth_real_power[idx]),
                "derivativeSpeed": float(smooth_derivative_speed[idx]),
                "derivativePower": float(smooth_derivative_power[idx]),
                "lateral": float(dataPoints[i].lateralAcle) if hasattr(dataPoints[i], 'lateralAcle') and dataPoints[i].lateralAcle not in (None, '') else 0.0,
                "long": float(dataPoints[i].longAcle) if hasattr(dataPoints[i], 'longAcle') and dataPoints[i].longAcle not in (None, '') else 0.0
            })

        lapJson = {
            "lap": int(lap.id),
            "points": points
        }

        all_laps.append(lapJson)

    return {"laps": all_laps}


def Potencia(Filepath_or_dataPoints, isFitFile=True, bikeConstants=BikeConstants()):
    if isinstance(Filepath_or_dataPoints, str):
        dataPoints = ReadFitFile(Filepath_or_dataPoints, isFitFile)
    else:
        dataPoints = Filepath_or_dataPoints

    if not dataPoints:
        return {"laps": []}

    roundedlist = listCoordinates(dataPoints)
    nPoints = len(dataPoints)

    # Calculate slopes and powers
    CalculateSlope(dataPoints, nPoints)
    maxGA = PotenciaGravidade(dataPoints, nPoints, bikeConstants)
    try:
        windFavor = calculateWindFavor(dataPoints, roundedlist)
    except Exception as e:
        print(f"Wind calculation warning: {e}")
        windFavor = [0.0] * nPoints

    maxRE = PowerResistenceAir(dataPoints, nPoints, bikeConstants, windFavor)
    PowerRollingRestiance(dataPoints, nPoints, bikeConstants)

    media, mediaReal = calculatePower(dataPoints, nPoints, bikeConstants)
    print("media calculda", media)
    print("media real", mediaReal)

    return toJson(dataPoints, nPoints)


if __name__ == "__main__":
    Potencia('power/real_power_27_06.fit')
