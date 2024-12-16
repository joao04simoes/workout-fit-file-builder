<template>
    <div class="mainContainer">
        <div class="input">
            <div class="button-group">
                <button for="messageInput" class="label" @click="saveValue">Step</button>
                <button for="RemoveAllSteps" class="label" @click="REmoveAllSteps">Remove all</button>
                <button for="fetchData" class="label" @click="openPopup">Send Data</button>
            </div>


            <div>
                <input class="tempInput" type="number" min="0" v-model="ValueMin" />
                :<input class="tempInput" type="number" min="0" max="59" v-model="ValueSeconds" />
            </div>
            <div>
                <label for="zoneDropdown">Select a Zone:</label>
                <select v-model="Valuezone" id="zoneDropdown">
                    <option v-for="zone in zones" :key="zone" :value="zone">{{ zone }}</option>
                </select>

            </div>
        </div>

        <div class="container">
            <div v-for="(value, index) in inter.Vmin" :key="index" class="rectangle" :style="{
                width: `${inter.Vmin[index] / 100}px`,   // Width based on Vmin
                height: `${inter.Vzone[index] * 20}px`, // Height based on Vzone
                backgroundColor: 'red',
                border: '1px solid white',
            }">
                <button for="removeStep " class="small-button" @click="removeStep(index)"> x </button>
                <button for="duplicate" class="small-button" @click="duplicateStep(index)"> c </button>
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
    <div>
        <input type="text" v-model="file_to_get" />
        <button @click="GetFile(file_to_get, 1)"> Get</button>
    </div>
    <div>
        <button @click="getAllNames"> All names</button>
    </div>
    <div>
        <ul v-if="AllfileNames">
            <li v-for="(value, key) in AllfileNames" :key="key">
                <button @click="showFitContent(key, value)" class="fileNameButton">{{ key }}, {{ value }}</button>
            </li>
        </ul>

    </div>
    <div v-if="FilePopUp > 0" class="popup-overlay">
        <div class="popupContentFile">
            <div class="container">
                <div v-for="(value, index) in Filedata.Vmin" :key="index" class="rectangle" :style="{
                    width: `${value / 100}px`,  // Use current Vmin value
                    height: `${Filedata.Vzones[index] * 20}px`, // Use corresponding Vzones value
                    backgroundColor: 'red',
                    border: '1px solid white',
                }">
                    <button for="removeStep " class="small-button" @click="removeStep(index)"> x </button>
                    <button for="duplicate" class="small-button" @click="duplicateStep(index)"> c </button>
                </div>
            </div>
            <button class="close-btn" @click="closePopup">X</button>

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
            FilePopUp: "0",
            ValueMin: "0",      // Minutes input
            Valuezone: "",     // Zone input
            ValueSeconds: "0",
            zones: [1, 2, 3, 4, 5],  // Seconds input
            AllfileNames: null,
            Filedata: null,
            data: null,
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
                        console.error("Error in response:", response.status, response.statusText);
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
