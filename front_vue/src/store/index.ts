import { createStore } from "vuex";
import { geomap } from "./geomap";
import { clone } from "@/helper";
import { router } from "../router";

const router_s2 = router;

export default createStore({
    state: {},
    getters: {},
    mutations: {},
    actions: {},
    modules: {
        geomap: geomap,
    },
});
