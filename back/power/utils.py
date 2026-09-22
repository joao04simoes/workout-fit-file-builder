from power.dataPoint import DataPoint
import numpy as np
from fit_tool.profile.messages.record_message import RecordMessage
from datetime import datetime, timezone


def distanceBetweenPoints(datapointx: DataPoint, datapointy: DataPoint):
    R = 6371e3

    def hav(theta):
        return np.sin(theta / 2) ** 2

    deltaLat = np.radians(datapointy.lat - datapointx.lat)
    deltaLong = np.radians(datapointy.long - datapointx.long)

    a = hav(deltaLat) + np.cos(np.radians(datapointx.lat)) * \
        np.cos(np.radians(datapointy.lat)) * hav(deltaLong)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c

    return d


def ReadFitFile(DataFitFile, dataPoints):
    print("Reading FIT file...")
    first = True
    for record in DataFitFile.records:
        if isinstance(record.message, RecordMessage):
            message = record.message
            point = DataPoint(
                time=message.timestamp,
                distance=message.distance or 0,
                realPower=message.power or 0,
                speed=message.speed or 0,
                cadence=message.cadence or 0,
                lat=message.position_lat or 0,
                long=message.position_long or 0,
                heart=message.heart_rate or 0,
                temperature=message.temperature or 0,
                altitude=message.altitude or 0
            )

            if point.power == 65535:
                point.power = 0

            if point.realPower == 65535:
                point.realPower = 0

            time = point.time / 1000
            if first:
                start_time = time
                first = False
            point.seconds = (time - start_time)
            iso_time = datetime.fromtimestamp(time, tz=timezone.utc).strftime(
                '%Y-%m-%dT%H:%M:%S.%f')[:-3] + ' GMT'
            point.time = iso_time

            if not (abs(point.lat) >= 179 or abs(point.long) >= 179):  # verify if data is valid
                dataPoints.append(point)

    print("Read complete. Data points:", len(dataPoints))


def ReadCsvFile(Filepath, dataPoints):
    print("Reading CSV file...")
    with open(Filepath, 'r') as file:
        for _ in range(11):
            next(file)
        for line in file:
            values = line.strip().split(',')
            point = DataPoint(
                time="2025-05-11T13:29:51.000 GMT",
                distance=float(values[6]),
                power=0,
                speed=float(values[7]),
                cadence=0,
                lat=float(values[12]),
                long=float(values[13]),
                heart=0,
                temperature=0,
                altitude=float(values[8]),
                lateralAcle=(values[18]),
                longAcle=(values[19])
            )
            dataPoints.append(point)
    print("Read complete. Data points:", len(dataPoints))


def derivative(dataPoints: list[DataPoint], nPoints: int):
    for i in range(1, nPoints-1):
        dataPoints[i].derivativeSpeed = (
            dataPoints[i+1].speed - dataPoints[i-1].speed) / 2
        dataPoints[i].derivativePower = (
            dataPoints[i+1].power - dataPoints[i-1].power) / 2
