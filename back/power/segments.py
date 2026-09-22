from power.dataPoint import DataPoint
from power.utils import distanceBetweenPoints
from fit_tool.profile.messages.record_message import RecordMessage
from datetime import datetime, timezone
import numpy as np


class Segments:
    def __init__(self, start=0, end=0, id=0):
        self.id = id
        self.start = start  # indice of the start of the segment
        self.end = end  # indice of the end of the segment
        self.time = 0
        self.AvgPower = 0
        self.AvgSpeed = 0
        self.AvgCadence = 0
        self.AvgHeart = 0

    def __str__(self):
        return (
            f"Segmento:{self.id}\n"
            f"  Start: {self.start}\n"
            f"  End: {self.end}\n"
            f"  Time: {self.time}\n"
            f"  Avg Power: {self.AvgPower}\n"
            f"  Avg Speed: {self.AvgSpeed * 3.6}\n"
            f"  Avg Cadence: {self.AvgCadence}\n"
            f"  Avg Heart: {self.AvgHeart}"
        )


def FindLaps(dataPoints: list[DataPoint], nPoints: int):
    margin = 10
    laps = []
    startLat = dataPoints[0].lat
    startLong = dataPoints[0].long
    lastPoint = dataPoints[0]
    startOfLap = 0
    endOfLap = -1

    print("Finding laps...")
    for i in range(1, nPoints):
        distance = distanceBetweenPoints(
            DataPoint(lat=startLat, long=startLong), dataPoints[i])
        if distance < margin and dataPoints[i].seconds > lastPoint.seconds + 100 and dataPoints[i].distance > lastPoint.distance + 1000:
            startLat = dataPoints[i].lat
            startLong = dataPoints[i].long
            lastPoint = dataPoints[i]
            if endOfLap == -1:
                laps.append({"start": startOfLap, "end": i})
                if i != nPoints:
                    startOfLap = i+1
                    endOfLap = -1
                else:
                    return laps

    print("Laps found:", len(laps))
    if (len(laps) == 0):
        laps.append({"start": 0, "end": nPoints-1})
        print("one lap")
    lapsSegment = []
    for i, lap in enumerate(laps):
        lapSegment = Segments(start=lap["start"], end=lap["end"], id=i)
        findAvgsMetricsOfSegment(lapSegment, dataPoints)
        lapsSegment.append(lapSegment)

    return lapsSegment


def findAvgsMetricsOfSegment(segment: Segments, dataPoints: list[DataPoint]):
    sumPower = []
    sumSpeed = 0
    sumCadence = 0
    sumHeart = 0
    nPoints = segment.end - segment.start + 1

    for i in range(segment.start, segment.end + 1):
        if dataPoints[i].power > 0:
            sumPower.append(dataPoints[i].power)
        sumSpeed += dataPoints[i].speed
        sumCadence += dataPoints[i].cadence
        sumHeart += dataPoints[i].heart

    sumPower = np.array(sumPower)

    segment.time = dataPoints[segment.end].seconds - \
        dataPoints[segment.start].seconds
    segment.AvgPower = sumPower.sum() / len(sumPower) if len(sumPower) > 0 else 0
    segment.AvgSpeed = sumSpeed / nPoints
    segment.AvgCadence = sumCadence / nPoints
    segment.AvgHeart = sumHeart / nPoints
