<template>
    <div>
        <button class="action-button" @click="GetPower">Load</button>

        <input type="text" name="filepath" v-model="Filepath" placeholder="path to .fit" />

        <div v-if="power?.laps?.length" style="margin-top: 16px;">
            <h3>Power (W) over distance</h3>
            <div ref="powerChartEl" style="width: 100%; height: 420px;"></div>

            <h3 style="margin-top: 24px;">Speed (km/h) over distance</h3>
            <div ref="speedChartEl" style="width: 100%; height: 420px;"></div>

            <h3 style="margin-top: 24px;">Derivative Speed (km/h) over distance</h3>
            <div ref="derivativeSpeedChartEl" style="width: 100%; height: 420px;"></div>

            <h3 style="margin-top: 24px;">Derivative Power (W) over distance</h3>
            <div ref="derivativePowerChartEl" style="width: 100%; height: 420px;"></div>

            <h3 style="margin-top: 24px;">Lateral Acceleration (m/s²) over distance</h3>
            <div ref="lateralChartEl" style="width: 100%; height: 420px;"></div>

            <h3 style="margin-top: 24px;">Longitudinal Acceleration (m/s²) over distance</h3>
            <div ref="longChartEl" style="width: 100%; height: 420px;"></div>

        </div>

        <div v-else-if="power && !power?.laps?.length" style="margin-top: 16px;">
            No laps returned.
        </div>
    </div>
</template>

<script>
import * as echarts from "echarts";
import { render } from "vue";

export default {
    name: "analyse",
    data() {
        return {
            Filepath: "",
            power: null,
            powerChart: null,
            speedChart: null,
            derivativeSpeedChart: null,
            derivativePowerChart: null,
            lateralChart: null,
            longChart: null,
        };
    },

    methods: {
        async GetPower() {
            try {
                const encodedPath = encodeURIComponent(this.Filepath);
                const response = await fetch(
                    `http://127.0.0.1:5000/api/potencia?path=${encodedPath}`,
                    { method: "GET" }
                );

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();
                this.power = data;

                // Render charts after DOM updates
                this.$nextTick(() => {
                    this.renderPowerChart();
                    this.renderSpeedChart();
                    this.renderDerivativeSpeedChart();
                    this.renderDerivativePowerChart();
                    this.renderLateralChart();
                    this.renderLongChart();

                });
            } catch (error) {
                console.error("Error during fetch:", error);
            }
        },

        buildSeries(metricKey, namePrefix) {
            // metricKey: "power" or "speed"
            // Converts laps -> ECharts series arrays: [ [time, value], ... ]
            return this.power.laps.map((lapObj) => ({
                name: `${namePrefix} ${lapObj.lap}`,
                type: "line",
                showSymbol: false,
                data: lapObj.points
                    .filter((p) => p.time != null && p[metricKey] != null)
                    .map((p) => [Number(p.time), Number(p[metricKey])]),
            }));
        },
        renderPowerChart() {
            const el = this.$refs.powerChartEl;
            if (!el) return;

            if (!this.powerChart) this.powerChart = echarts.init(el);

            const series = this.buildSeries("power", "Lap");
            const series2 = this.buildSeries("realPower", "Lap");

            series.forEach(s => {
                s.lineStyle = {
                    ...(s.lineStyle || {}),
                    width: 2
                };
                s.itemStyle = {
                    ...(s.itemStyle || {}),
                    color: "#5470C6"
                };
            });

            series2.forEach(s => {
                s.lineStyle = {
                    ...(s.lineStyle || {}),
                    width: 2,
                    type: "dashed"
                };
                s.itemStyle = {
                    ...(s.itemStyle || {}),
                    color: "#EE6666"
                };
            });

            this.powerChart.setOption({
                tooltip: { trigger: "axis" },
                legend: { top: 10 },
                xAxis: {
                    type: "value",
                    name: "Time (s)"
                },
                yAxis: {
                    type: "value",
                    name: "Power (W)"
                },
                dataZoom: [
                    { type: "inside" },
                    { type: "slider" }
                ],
                series: [...series, ...series2]
            }, true);

            this.powerChart.resize();
        },

        renderSpeedChart() {
            const el = this.$refs.speedChartEl;
            if (!el) return;

            if (!this.speedChart) this.speedChart = echarts.init(el);

            const series = this.buildSeries("speed", "Lap").map((s) => ({
                ...s,
                // If your backend speed is m/s, convert to km/h here:
                // data: s.data.map(([t, v]) => [t, v * 3.6]),
            }));

            this.speedChart.setOption(
                {
                    tooltip: { trigger: "axis" },
                    legend: { top: 10 },
                    xAxis: { type: "value", name: "Time (s)" },
                    yAxis: { type: "value", name: "Speed (km/h or m/s)" },
                    dataZoom: [{ type: "inside" }, { type: "slider" }],
                    series,
                },
                true
            );
            this.speedChart.resize();
        },

        renderDerivativeSpeedChart() {
            const el = this.$refs.derivativeSpeedChartEl;
            if (!el) return;

            if (!this.derivativeSpeedChart) this.derivativeSpeedChart = echarts.init(el);
            const series = this.buildSeries("derivativeSpeed", "Lap").map((s) => ({
                ...s,
                // If your backend speed is m/s, convert to km/h here:
                // data: s.data.map(([t, v]) => [t, v * 3.6]),
            }));

            this.derivativeSpeedChart.setOption(
                {
                    tooltip: { trigger: "axis" },
                    legend: { top: 10 },
                    xAxis: { type: "value", name: "Time (s)" },
                    yAxis: { type: "value", name: " Derivative Speed (km/h or m/s)" },
                    dataZoom: [{ type: "inside" }, { type: "slider" }],
                    series,
                },
                true
            );
            this.derivativeSpeedChart.resize();
        },

        renderDerivativePowerChart() {
            const el = this.$refs.derivativePowerChartEl;
            if (!el) return;

            if (!this.derivativePowerChart) this.derivativePowerChart = echarts.init(el);
            const series = this.buildSeries("derivativePower", "Lap");

            this.derivativePowerChart.setOption(
                {
                    tooltip: { trigger: "axis" },
                    legend: { top: 10 },
                    xAxis: { type: "value", name: "Time (s)" },
                    yAxis: { type: "value", name: "Derivative Power (W/s)" },
                    dataZoom: [{ type: "inside" }, { type: "slider" }],
                    series,
                },
                true
            );
            this.derivativePowerChart.resize();
        },

        renderLateralChart() {
            const el = this.$refs.lateralChartEl;
            if (!el) return;

            if (!this.lateralChart) this.lateralChart = echarts.init(el);
            const series = this.buildSeries("lateral", "Lap");

            this.lateralChart.setOption(
                {
                    tooltip: { trigger: "axis" },
                    legend: { top: 10 },
                    xAxis: { type: "value", name: "Time (s)" },
                    yAxis: { type: "value", name: "Lateral (m)" },
                    dataZoom: [{ type: "inside" }, { type: "slider" }],
                    series,
                },
                true
            );
            this.lateralChart.resize();
        },

        renderLongChart() {
            const el = this.$refs.longChartEl;
            if (!el) return;

            if (!this.longChart) this.longChart = echarts.init(el);
            const series = this.buildSeries("long", "Lap");

            this.longChart.setOption(
                {
                    tooltip: { trigger: "axis" },
                    legend: { top: 10 },
                    xAxis: { type: "value", name: "Time (s)" },
                    yAxis: { type: "value", name: "Longitudinal (m)" },
                    dataZoom: [{ type: "inside" }, { type: "slider" }],
                    series,
                },
                true
            );
            this.longChart.resize();
        },
    },

    mounted() {
        window.addEventListener("resize", () => {
            this.powerChart?.resize();
            this.speedChart?.resize();
            this.derivativeSpeedChart?.resize();
            this.derivativePowerChart?.resize();
        });
    },

    beforeUnmount() {
        window.removeEventListener("resize", () => { });
        this.powerChart?.dispose();
        this.speedChart?.dispose();
        this.derivativeSpeedChart?.dispose();
        this.derivativePowerChart?.dispose();
    },
};
</script>
