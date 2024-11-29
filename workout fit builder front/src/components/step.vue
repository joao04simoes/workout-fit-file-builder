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

        <div class="container">
            <div v-for="(value, index) in inter.Vmin" :key="index" class="rectangle" :style="{
                width: `${inter.Vmin[index] / 100}px`,   // Width based on Vmin
                height: `${inter.Vzone[index] * 20}px`, // Height based on Vzone
                backgroundColor: 'red',
                border: '1px solid white',
            }">
                <button for="removeStep " class="small-button" @click="removeStep(index)"> x </button>
            </div>
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
        removeStep(index) {
            this.inter.Vmin.splice(index, 1)
            this.inter.Vzone.splice(index, 1)
        },
    },
};
</script>

<style scoped>
.small-button {
    font-size: 6px;
    padding: 5px 5px;
    background-color: #f0f0f0;
    color: #333;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.2s ease;

}

.small-button:active {
    transform: scale(0.95);
    /* Shrinks slightly when clicked */
}

.container {
    display: flex;
    /* Enable Flexbox */
    align-items: flex-end;
    /* Align all items to the bottom */
}

.rectangle {
    display: flex;
    /* Allow button placement inside */
    justify-content: center;
    /* Center the button horizontally */
    align-items: flex-start;
    /* Position button at the top of the block */
    flex-direction: column-reverse;
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
