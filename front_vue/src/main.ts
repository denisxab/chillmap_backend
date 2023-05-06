import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import {router} from "./router";

export let app = createApp(App);

app.use(router) // Подключаем ройтер страниц к приложению
    .use(store)
    .mount("#app");
