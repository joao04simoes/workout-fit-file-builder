import math
from power.forces import CalculateSlope, PotenciaGravidade, PowerResistenceAir, PowerRollingRestiance
from fit_tool.fit_file import FitFile
from fit_tool.profile.messages.record_message import RecordMessage
from datetime import datetime, timezone


class BikeConstants:
    def __init__(self, G=9.81, weight=90, CdA=0.32, density=1.240088, Crr=0.005, losses=0.05):
        self.G = G
        self.weight = weight
        self.CdA = CdA
        self.density = density
        self.Crr = Crr
        self.losses = losses


class DataPoint:
    def __init__(self, time=0, lat=0, long=0, heart=0, power=0, cadence=0, distance=0, temperature=0, speed=0, altitude=0, slope=0, powerGravity=0, powerAir=0, powerRR=0):
        self.time = time
        self.lat = float(lat)
        self.long = float(long)
        self.heart = int(heart)
        self.cadence = cadence
        self.power = power
        self.distance = float(distance)
        self.temperature = int(temperature)
        self.speed = float(speed)
        self.altitude = float(altitude)
        self.slope = float(slope)  # radians
        self.powerGravity = float(powerGravity)
        self.powerAir = float(powerAir)
        self.powerRR = float(powerRR)

    def __repr__(self):
        return (f"DataPoint(time={self.time}, lat={self.lat}, long={self.long}, "
                f"heart={self.heart}, cadence={self.cadence}, distance={self.distance}, "
                f"temperature={self.temperature}, speed={self.speed}, altitude={self.altitude})")


def listCoordinates(dataPoints):
    roundedlist = list(
        {(round(item.lat, 2), round(item.long, 2)) for item in dataPoints})
    print(roundedlist)
    return roundedlist


def ReadFitFile(DataFitFile, dataPoints):
    print("Reading FIT file...")
    for record in DataFitFile.records:
        if isinstance(record.message, RecordMessage):
            message = record.message
            point = DataPoint(
                time=message.timestamp,
                distance=message.distance or 0,
                power=message.power or 0,
                speed=message.speed or 0,
                cadence=message.cadence or 0,
                lat=message.position_lat or 0,
                long=message.position_long or 0,
                heart=message.heart_rate or 0,
                temperature=message.temperature or 0,
                altitude=message.altitude or 0
            )

            time = point.time / 1000

            iso_time = datetime.fromtimestamp(time, tz=timezone.utc).strftime(
                '%Y-%m-%dT%H:%M:%S.%f')[:-3] + ' GMT'
            point.time = iso_time
            dataPoints.append(point)
    print("Read complete. Data points:", len(dataPoints))


def Potencia(Filepath):
    bikeConstants = BikeConstants()
    dataPoints = []
    # path = '/home/joaosimoes/Downloads/Campeonato_nacional_xco.fit'

    # Read FIT file
    fit_file = FitFile.from_file(Filepath)
    ReadFitFile(fit_file, dataPoints)
    print(dataPoints[2])

    if not dataPoints:
        print("No data points found.")
        return

    print("Data points read successfully.")

    roundedlist = listCoordinates(dataPoints)
    nPoints = len(dataPoints)

    # Calculate slopes and powers
    CalculateSlope(dataPoints, nPoints)
    maxGA = PotenciaGravidade(dataPoints, nPoints, bikeConstants)
    maxRE = PowerResistenceAir(dataPoints, nPoints, bikeConstants, roundedlist)
    PowerRollingRestiance(dataPoints, nPoints, bikeConstants)

    # Analyze power data
    Power = []
    PositivePower = []
    Tempo = []
    sumPower = 0
    nPositive = 0
    mediaBpm = 0
    mediaSpeed = 0

    for i in range(0, nPoints-1):
        tem = i
        power = (dataPoints[i].powerGravity +
                 dataPoints[i].powerAir + dataPoints[i].powerRR) * (bikeConstants.losses + 1)
        Power.append(power)
        mediaBpm = mediaBpm + dataPoints[i].heart
        mediaSpeed = mediaSpeed + dataPoints[i].speed
        if power > 0:
            sumPower = sumPower + power
            nPositive = nPositive + 1
            Tempo.append(tem)
            PositivePower.append(power)

    media = sumPower/nPositive
    mediaBpm = mediaBpm/nPoints
    mediaSpeed = (mediaSpeed/nPoints)*3.6
    print("BPM:", mediaBpm)
    print("Speed:", mediaSpeed)
    print(media)
    return PositivePower


# if __name__ == "__main__":
 #   main()
