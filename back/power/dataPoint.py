class DataPoint:
    def __init__(self, time=0, lat=0, long=0, heart=0, realPower=0, power=0, cadence=0, distance=0, temperature=0, speed=0, altitude=0, slope=0, powerGravity=0, powerAir=0, powerRR=0, lateralAcle="0", longAcle="0"):
        self.time = time
        self.lat = float(lat)
        self.long = float(long)
        self.heart = int(heart)
        self.cadence = cadence
        self.realPower = realPower
        self.power = power
        self.distance = float(distance)
        self.temperature = int(temperature)
        self.speed = float(speed)
        self.altitude = float(altitude)
        self.slope = float(slope)  # radians
        self.powerGravity = float(powerGravity)
        self.powerAir = float(powerAir)
        self.powerRR = float(powerRR)
        self.seconds = 0
        self.derivativeSpeed = 0
        self.derivativePower = 0
        self.lateralAcle = lateralAcle
        self.longAcle = longAcle

    def __repr__(self):
        return (f"DataPoint(time={self.time}, lat={self.lat}, long={self.long}, "
                f"heart={self.heart}, cadence={self.cadence}, distance={self.distance}, "
                f"temperature={self.temperature}, speed={self.speed}, altitude={self.altitude})")
