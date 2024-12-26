<template>
    <div class="main-container">
        <!-- Input Section -->
        <div class="input-section">
            <div class="button-group">
                <button class="action-button" @click="saveValue">Step</button>
                <button class="action-button" @click="REmoveAllSteps">Remove all</button>
                <button class="action-button" @click="openPopup">Send Data</button>
            </div>
            <div class="input-group">
                <input class="time-input" type="number" min="0" v-model="interval" placeholder="numero de intervalos" />
                <input class="time-input" type="number" min="0" v-model="multiplier" placeholder="multi" />
                <div v-for="(value, index) in interval  " :key="index">
                    <input class="time-input" type="number" min="0" v-model="ValueMin[index]" placeholder="Minutes" />
                    <span>:</span>
                    <input class="time-input" type="number" min="0" max="59" v-model="ValueSeconds[index]"
                        placeholder="Seconds" />

                    <div class="zone-selection">
                        <label for="zoneDropdown">Select a Zone:</label>
                        <select v-model="Valuezone[index]" id="zoneDropdown" class="zone-dropdown">
                            <option v-for="zone in zones" :key="zone" :value="zone">{{ zone }}</option>
                        </select>
                    </div>
                </div>

            </div>

        </div>


        <div class="rectangle-container">
            <div v-for="(value, index) in inter.Vmin" :key="index" class="rectangle" :style="{
                width: `${inter.Vmin[index] / 100}px`,
                height: `${inter.Vzone[index] * 20}px`
            }">
                <div class="rectangle-buttons">
                    <button class="small-button" @click="removeStep(index)">✖</button>
                    <button class="small-button" @click="duplicateStep(index)">⧉</button>
                </div>
            </div>
        </div>
        <div v-if="isVisible" class="popup-overlay">
            <div class="popup-content">
                <label>Filename</label>
                <input type="text" v-model="inter.FileName" />
                <button class="close-btn" @click="sendData">X</button>

            </div>
        </div>
    </div>
</template>


<script>
export default {
    name: "Step",
    data() {
        return {
            //file_to_get: "",
            isVisible: false,
            interval: 1,
            ValueMin: [],      // Minutes input
            Valuezone: [],     // Zone input
            ValueSeconds: [],
            multiplier: 1,
            zones: [1, 2, 3, 4, 5],  // Seconds input
            inter: {
                Vmin: [],  // Array for rectangle widths (calculated from minutes & seconds)
                Vzone: [], // Array for rectangle heights (from zone)
                FileName: "",
            },
        };
    },


    computed: {
        jsonData() {
            return JSON.stringify(this.inter, null, 2); // Format JSON data for display
        },
    },
    methods: {
        openPopup() {
            if (this.inter.Vmin.length > 0) {
                this.isVisible = true; // Abre o pop-up
            }
        },


        async GetFile(FileName, func) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/fitFile?filename=${FileName}&func=${func}`, {
                    method: "GET",
                })
                if (response.ok && func == 1) {
                    const blob = await response.blob();
                    const link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = `${FileName}.fit`;
                    link.click();
                } else {
                    console.error("Error in response:", response.status, response.statusText);
                }
            } catch (error) {
                console.error("Error during fetch:", error);
            }

        },


        async sendData() {
            this.isVisible = false
            if (this.inter.Vmin.length > 0 && this.inter.Vzone.length > 0) {
                try {
                    // Send JSON data to the backend
                    const jsonData = JSON.stringify(this.inter);

                    console.log("Sending data:", jsonData); // Debug output

                    // Enviar requisição POST para o backend
                    const response = await fetch("http://127.0.0.1:5000/api/data", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: jsonData,
                    });
                    if (response.ok) {
                        const blob = await response.blob();
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = `${this.inter.FileName}.fit`;
                        link.click();
                    } else {
                        this.inter.Vmin.push(totalSeconds);
                        this.inter.Vzone.push(parseInt(this.Valuezone, 10)); console.error("Error in response:", response.status, response.statusText);
                    }
                    this.inter.FileName = ""
                } catch (error) {
                    console.error("Error during fetch:", error);
                }
            } else {
                console.error("Array vazio  ");
            }
        },

        saveValue() {
            if (this.ValueMin.length > 0 && this.Valuezone.length > 0) {
                for (let j = 0; j < this.multiplier; j++) {
                    for (let i = 0; i < this.interval; i++) {
                        if (this.ValueSeconds[i] > -1) {
                            const totalSeconds = (parseInt(this.ValueMin[i], 10) * 1000) +
                                (parseInt(this.ValueSeconds[i], 10) / 60 * 1000);
                            this.inter.Vmin.push(totalSeconds);
                            this.inter.Vzone.push(parseInt(this.Valuezone[i] || 0, 10));
                        }
                    }
                }
                this.ValueMin = [];
                this.ValueSeconds = [];
                this.Valuezone = [];
            } else {
                console.error("Inputs for minutes and zones are missing or empty.");
            }
        },

        removeStep(index) {
            this.inter.Vmin.splice(index, 1)
            this.inter.Vzone.splice(index, 1)
        },
        duplicateStep(index) {
            this.inter.Vmin.push(this.inter.Vmin[index])
            this.inter.Vzone.push(this.inter.Vzone[index])
        },
        REmoveAllSteps() {
            this.inter.Vmin = []
            this.inter.Vzone = []
        },
    },
};
</script>

<style></style>
