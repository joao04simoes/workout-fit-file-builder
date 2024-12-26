<template>
    <div class="barraHead">
        <nav class="navLinks">
            <router-link class="navLink" to="/joao.simoes/">Workout Builder</router-link>
            <router-link class="navLink" to="/joao.simoes/get/">Get Files</router-link>
            <router-link class="navLink" to="/joao.simoes/analyse/">Analyse</router-link>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'headComp',
};
</script>

<style>
.barraHead {
    display: flex;
    align-items: center;
    width: 100%;
    height: 50px;
    background-color: #007bff;
    border-radius: 5px;
    padding: 0 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


.navLinks {
    display: flex;
    gap: 20px;
}


.navLink {
    color: white;
    text-decoration: none;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 15px;
    border-radius: 5px;
    transition: background-color 0.3s ease, color 0.3s ease;
}


.navLink:hover {
    background-color: white;
    color: #007bff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}


.navLink.router-link-active {
    background-color: #0056b3;
    color: white;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
}
</style>
