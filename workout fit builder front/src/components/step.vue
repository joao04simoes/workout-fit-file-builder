<template>
    <div>
        <button for="messageInput" class="label" @click="saveValue">Step</button>
        <button for="fetchData" class="label" @click="sendData">Send Data</button>

        <div>
            <input id="min" type="number" min="0" v-model="ValueMin" placeholder="Minutes" />
            :<input id="seconds" type="number" min="0" max="59" v-model="ValueSeconds" placeholder="Seconds" />
        </div>
        <div>
            <label for="zoneDropdown">Select a Zone:</label>
            <select v-model="Valuezone" id="zoneDropdown">
                <option v-for="zone in zones" :key="zone" :value="zone">{{ zone }}</option>
            </select>

        </div>


        <div v-for="(value, index) in inter.Vmin" :key="index" class="rectangle" :style="{
            width: `${inter.Vmin[index] / 100}px`,   // Width based on Vmin
            height: `${inter.Vzone[index] * 10}px`, // Height based on Vzone
            backgroundColor: 'red',
        }">
        </div>

        <pre>{{ jsonData }}</pre>
    </div>
</template>

<script>
export default {
    name: "Step",
    data() {
        return {
            ValueMin: "0",      // Minutes input
            Valuezone: "",     // Zone input
            ValueSeconds: "0",
            zones: [1, 2, 3, 4, 5],  // Seconds input
            inter: {
                Vmin: [],  // Array for rectangle widths (calculated from minutes & seconds)
                Vzone: [], // Array for rectangle heights (from zone)
            },
        };
    },
    computed: {
        jsonData() {
            return JSON.stringify(this.inter, null, 2); // Format JSON data for display
        },
    },
    methods: {
        async sendData() {
            // Send JSON data to the backend
            const jsonData = JSON.stringify(this.inter);
            console.log("Sending data:", jsonData); // Debug output
            await fetch("http://127.0.0.1:5000/api/data", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: jsonData,
            });
        },

        saveValue() {

            if (this.ValueMin !== "" && this.Valuezone !== "") {
                if (this.ValueSeconds == "") {
                    this.ValueSeconds = 0
                }

                const totalSeconds = (parseInt(this.ValueMin, 10) * 1000) + (parseInt(this.ValueSeconds, 10) / 60 * 1000);


                this.inter.Vmin.push(totalSeconds);
                this.inter.Vzone.push(parseInt(this.Valuezone, 10));
                // Clear input fields
                this.ValueMin = "";
                this.Valuezone = "";
                this.ValueSeconds = "";
            }
        },
    },
};
</script>

<style scoped>
.rectangle {
    display: inline-block;

}

.label {
    font-weight: bold;
    margin-bottom: 10px;
}

input {
    margin-bottom: 10px;
    padding: 5px;
    font-size: 1em;
}

button {
    padding: 5px 10px;
    font-size: 1em;
    margin-bottom: 15px;
}

ul {
    margin-top: 10px;
    list-style-type: none;
    padding: 0;
}
</style>
