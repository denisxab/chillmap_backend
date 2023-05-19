import { createRouter, createWebHistory } from "vue-router";
import VueRouter from "vue-router";
import MapApp from "@/pages/MapApp.vue";
import SelectChenel from "@/pages/SelectChenel.vue";

const routes: VueRouter.RouteRecordRaw[] = [
    /*
    Сюда добавляем пути к компанентам
    */
    // Статичный путь.
    // {
    //     path: "/Путь",
    //     component: КомпанентVue,
    // },
    // Динамический путь. Вместо `id` можно указать любое имя, результат будет храниться в `$route.params`
    // {
    //     path: "/home",
    //     // component: MapApp,
    //     redirect: { name: "main" },
    // },
    {
        path: '/channels',
        name: 'list_channels',
        component: SelectChenel
    },
    {
        path: "/",
        name: "main_map",
        component: MapApp,
        // redirect: { name: "main_map" },
    },


    // {
    // path: "/map",
    // },
];

export const router = createRouter({
    routes,
    history: createWebHistory(),
});
// export default router;
