import { createRouter, createWebHistory } from 'vue-router';

// Import your components
import Step from '../components/step.vue';
import get from '../components/get.vue'


// Define routes
const routes = [
    { path: '/joao.simoes/', name: 'Step', component: Step },
    { path: '/joao.simoes/get', name: 'get', component: get }
];

// Create the router instance
const router = createRouter({
    history: createWebHistory(), // Use history mode for clean URLs
    routes,
});

export default router;
