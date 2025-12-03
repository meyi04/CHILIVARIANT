import { createRouter, createWebHistory } from "vue-router";
import Landing from "./pages/Landing.vue";
import Home from "./pages/Home.vue";
import Input from "./pages/Input.vue";
import History from "./pages/History.vue";
import Analytics from "./pages/Analytics.vue";

const routes = [
    { path: "/", component: Landing },  // Landing as initial page
    { path: "/home", component: Home },
    { path: "/input", component: Input },
    { path: "/history", component: History },
    { path: "/analytics", component: Analytics },
];

export default createRouter({
    history: createWebHistory(),
    routes,
});