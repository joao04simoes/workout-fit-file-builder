<template>
    <div>
        <button class="action-button" @click="GetPower"></button>
        <input type="text" name="filepath" v-model="Filepath">
        <div v-if="power">

        </div>
    </div>
</template>
<script>
export default {
    name: "analyse",
    data() {
        return {
            Filepath: "",
            power: null,
        }
    },

    methods: {
        async GetPower() {
            try {
                const encodedPath = encodeURIComponent(this.Filepath);
                const response = await fetch(`http://127.0.0.1:5000/api/potencia?path=${encodedPath}`, {
                    method: "GET",
                })
                const data = await response.json();
                this.power = data;
            } catch (error) {
                console.error("Error during fetch:", error);
            }
        },
    }
};
</script>