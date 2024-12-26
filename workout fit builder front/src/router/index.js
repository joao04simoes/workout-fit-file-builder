import { createRouter, createWebHistory } from 'vue-router';

// Import your components
import Step from '../components/step.vue';
import get from '../components/get.vue'
import analyse from '../components/analyse.vue'


// Define routes
const routes = [
    { path: '/joao.simoes/', name: 'Step', component: Step },
    { path: '/joao.simoes/get', name: 'get', component: get },
    { path: '/joao.simoes/analyse/', name: 'analyse', component: analyse },
];

// Create the router instance
const router = createRouter({
    history: createWebHistory(), // Use history mode for clean URLs
    routes,
});

export default router;
