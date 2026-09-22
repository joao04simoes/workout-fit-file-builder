import numpy as np
from power.main import BikeConstants, ReadFitFile, Potencia, listCoordinates, calculatePower, moving_average_np
from power.forces import CalculateSlope, PotenciaGravidade, PowerResistenceAir, PowerRollingRestiance, calculateWindFavor
import os
import matplotlib.pyplot as plt
FilePaths = ["./workout-fit-file-builder/back/bmc_estrada/real_power_6_07.fit",
             "./workout-fit-file-builder/back/bmc_estrada/real_power_5_07.fit", "./workout-fit-file-builder/back/bmc_estrada/real_power_4_07.fit"]
FilePaths_ = ["./workout-fit-file-builder/back/bmc_xco/real_power_27_06.fit",
              "./workout-fit-file-builder/back/bmc_xco/real_power_28_06.fit"]

isFitFile = True

# verify if the files exist
if not all([os.path.exists(file) for file in FilePaths]):
    print("One or more files do not exist. Please check the file paths.")
    exit(1)

CRR = [
    0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.02]
CDA = [0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32]
losses = [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05]

# CRR = [0.015]
# CDA = [0.2]
# losses = [0.02]

results = np.zeros((len(CRR), len(CDA), len(losses)))
best = [0, 0, 0]
bestScore = float("inf")
for FilePath in FilePaths:
    print(f"Processing file: {FilePath}")

    dataPoints = ReadFitFile(FilePath, True)
    counter = 0
    allCadencia = 0
    for point in dataPoints:
        if point.cadence < 1:
            counter += 1
        else:
            allCadencia += point.cadence

    print(f"number of 0 cadence", counter)
    print(f"average cadence", allCadencia/(len(dataPoints) - counter))

    bikeConstants = BikeConstants()

    roundedlist = listCoordinates(dataPoints)
    nPoints = len(dataPoints)

    CalculateSlope(dataPoints, nPoints)
    sampleDistance = [point.distance for point in dataPoints]

    slopeSeries = [np.tan(point.slope)*100 for point in dataPoints]
    slopeSeries_moving_avg = moving_average_np(slopeSeries, window=15)

    for point, slope in zip(dataPoints, slopeSeries_moving_avg):
        point.slope = np.arctan(slope / 100)  # Convert back to radians
    # plt.figure(figsize=(10, 5))
    # plt.plot(sampleDistance, slopeSeries_moving_avg,
    #         label='Slope', color='blue')
    # plt.title('Slope over Distance')
    # plt.xlabel('Distance (m)')
    # plt.ylabel('Slope')
    # plt.legend()
    # plt.grid()
    # plt.show()
#
    windFavor = calculateWindFavor(dataPoints, roundedlist)

    PotenciaGravidade(dataPoints, nPoints, bikeConstants)

    diferenca = 9999
    for i, crr in enumerate(CRR):
        for j, cda in enumerate(CDA):
            for k, loss in enumerate(losses):
                print(
                    f"Testing parameters: Crr={crr}, CdA={cda}, Losses={loss}")
                bikeConstants = BikeConstants(Crr=crr, CdA=cda, losses=loss)
                PowerResistenceAir(dataPoints, nPoints,
                                   bikeConstants, windFavor)
                PowerRollingRestiance(dataPoints, nPoints, bikeConstants)
                media, mediaReal = calculatePower(
                    dataPoints, nPoints, bikeConstants)

                # Calculate error weighted by segment length (meters)
                distances = np.array([dp.distance for dp in dataPoints])
                # segment lengths (prepend first delta to keep same length)
                deltas = np.diff(distances, prepend=distances[0])
                # avoid zero or negative deltas
                deltas[deltas <= 0] = 1e-3

                errors = np.array(
                    [dp.power - dp.realPower for dp in dataPoints])
                weighted_sq = (errors ** 2) * deltas

                total_distance = distances[-1] - distances[0]
                if total_distance <= 0:
                    total_distance = deltas.sum()

                # Mean squared error per meter and root MSE per meter
                mse_per_meter = weighted_sq.sum() / total_distance
                rmse_per_meter = np.sqrt(mse_per_meter)

                results[i][j][k] = mse_per_meter
                print(
                    f"Score (MSE/m): {mse_per_meter:.6f}, RMSE/m: {rmse_per_meter:.6f}")

top10 = []
for i, crr in enumerate(CRR):
    for j, cda in enumerate(CDA):
        for k, loss in enumerate(losses):
            score = results[i][j][k]
            top10.append((score, i, j, k))
            if score < bestScore:
                bestScore = results[i][j][k]
                best = [i, j, k]

top10.sort(key=lambda item: item[0])
top10 = top10[:10]


print(
    f"Best parameters found: Crr={CRR[best[0]]}, CdA={CDA[best[1]]}, Losses={losses[best[2]]}")
print(f"Best score: {bestScore}")

print("Top 10 parameter combinations:")
for rank, (score, i, j, k) in enumerate(top10, start=1):
    print(
        f"{rank:02d}. score={score:.6f} | Crr={CRR[i]} | CdA={CDA[j]} | Losses={losses[k]}"
    )

X = np.array([
    [
        dp.lat if abs(dp.lat) < 179 else np.nan,
        dp.long if abs(dp.long) < 179 else np.nan,
        dp.heart,
        dp.cadence,
        dp.power,
        dp.speed,
        dp.altitude,
        dp.slope,
        dp.distance,
        dp.time,

    ]
    for dp in dataPoints
])

if __name__ == "__main__":
    print("Running the script directly.")
