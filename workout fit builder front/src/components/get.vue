<template>

    <div>
        <input class="Textinput" type="text" v-model="file_to_get" />
        <button class="action-button" @click="GetFile(file_to_get, 1)"> Get</button>
    </div>
    <div>
        <button class="action-button" @click="getAllNames"> All names</button>
    </div>
    <div>
        <ul v-if="AllfileNames">
            <li v-for="(value, key) in AllfileNames" :key="key">
                <button class="action-button" @click="showFitContent(key, value)">{{ key }}, {{
                    value }}</button>
            </li>
        </ul>

    </div>
    <div v-if="FilePopUp > 0" class="popup-overlay">
        <div class="popupContentFile">
            <div class="rectangle-container">
                <div v-for="(value, index) in Filedata.Vmin" :key="index" class="rectangle" :style="{
                    width: `${value / 100}px`,  // Use current Vmin value
                    height: `${Filedata.Vzones[index] * 20}px`, // Use corresponding Vzones value
                    backgroundColor: 'red',
                    border: '1px solid white',
                }">
                    {{ value }} * zone {{ Filedata.Vzones[index] }}
                </div>
            </div>
            <button class="action-button" @click="closePopup">X</button>

        </div>

    </div>
</template>
<script>
export default {
    name: "get",
    data() {
        return {
            //file_to_get: "",
            isVisible: false,
            FilePopUp: "0",

            AllfileNames: null,
            Filedata: null,
            data: null,

        };
    },


    methods: {

        showFitContent(key, value) {
            this.GetFile(value, 2)
            this.FilePopUp = key
        },

        openPopup() {
            this.isVisible = true; // Abre o pop-up
        },
        closePopup() {
            this.FilePopUp = 0
        },
        async getAllNames() {
            try {

                const response = await fetch(`http://127.0.0.1:5000/api/getAll`, {
                    method: "GET",
                })
                if (response.ok) {
                    this.AllfileNames = await response.json();


                } else {
                    console.error("Error in response:", response.status, response.statusText);
                }
            } catch (error) {
                console.error("Error during fetch:", error);
            }

        },

        async GetFile(FileName, func) {

            try {

                const response = await fetch(`http://127.0.0.1:5000/api/fitFile?filename=${FileName}&func=${func}`, {
                    method: "GET",
                })
                if (response.ok && func == 2) {
                    this.data = await response.json()
                    this.Filedata = {
                        Vmin: JSON.parse(this.data.Vmin),   // Convert string to array
                        Vzones: JSON.parse(this.data.Vzones) // Convert string to array
                    };

                }
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
    }


};
</script>

<style>
.Textinput {
    background: #f7f7f7;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 8px 12px;
    font-size: 1rem;
    width: 200px;
    text-align: center;
    outline: none;
}
</style>