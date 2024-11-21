<template>
    <div>

        <button for="messageInput" class="label" @click="saveValue">Step</button>


        <div>
            <input id="min" v-model="ValueMin" placeholder="minutos" />
        </div>
        <div>
            <input id="zone" v-model="Valuezone" placeholder="zona" />
        </div>


        <h3>Array 1 (Minutes):</h3>
        <ul>
            <li v-for="(item, index) in Vmin" :key="'array1-' + index">{{ item }}</li>
        </ul>


        <h3>Array 2 (Zones):</h3>
        <ul>
            <li v-for="(item, index) in Vzones" :key="'array2-' + index">{{ item }}</li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "Step",
    data() {
        return {
            ValueMin: "",
            Valuezone: "",
            Vmin: [],
            Vzones: [],
        };
    },
    methods: {
        saveValue() {

            if (this.ValueMin.trim() !== "" && this.Valuezone.trim() !== "") {
                this.Vmin.push(this.ValueMin);
                this.Vzones.push(this.Valuezone);
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