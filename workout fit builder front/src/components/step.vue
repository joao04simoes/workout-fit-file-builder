<template>
    <div>

        <button for="messageInput" class="label" @click="saveValue">Step</button>
        <button for="fetchData" class="label" @click="sendData">Send Data</button>

        <div>
            <input id="min" v-model="ValueMin" placeholder="minutos" />
        </div>
        <div>
            <input id="zone" v-model="Valuezone" placeholder="zona" />
        </div>



        <pre> {{ jsonData }}</pre>
    </div>
</template>

<script>


export default {
    name: "Step",
    data() {
        return {
            ValueMin: "",
            Valuezone: "",
            "inter": {
                Vmin: [],
                Vzones: [],
            }
        };
    },
    computed: {
        jsonData() {
            return JSON.stringify(this.inter, null, 2);
        },
    },
    methods: {
        async sendData() {
            const jsonData = JSON.stringify(this.inter)
            console.log("Sending data:", jsonData); // Debug output
            // Example using fetch to send JSON
            await fetch('http://127.0.0.1:5000/api/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: jsonData,
            });
        },


        saveValue() {

            if (this.ValueMin.trim() !== "" && this.Valuezone.trim() !== "") {
                this.inter.Vmin.push(this.ValueMin);
                this.inter.Vzones.push(this.Valuezone);
                this.ValueMin = "";
                this.Valuezone = "";
            }
        },
    },
};
</script>

<style scoped>
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