import {
    TCoord,
    Tgeomap,
    Tmeta_geomapJson,
    TPropertiesMark,
    UrlGetParams,
    UrlGetParamsTypeView,
} from "@/interface";
import { ParseUrlSrc, clone } from "@/helper";

export const geomap = {
    // Доступные переменные в хранилище
    state() {
        return {
            // Поверхностная информация о местах
            geomap_json: <Tgeomap>{},
            // Мета данные
            meta_data_json: <Tmeta_geomapJson>{},
            // Текущие выбранное место
            select_PropertiesMark: <TPropertiesMark>undefined,
            // Координаты на которое совершено нажатие, или фокусировка
            coordinat_click: <TCoord>{
                latitude: 59.859292472503114,
                longitude: 30.169246265131953,
            },
            // Текущие приближение карты
            zoom_select: <number>16,
            // Режим просмотра
            type_view: <string>UrlGetParamsTypeView.main_map,
            // Текущий id группы для просмотра
            select_geomap_id: <number>undefined,
            // Ссылка для скачивания geomap
            url_geomap: <string>undefined,
        };
    },
    mutations: {
        Update_geomap_json(state, newValue: Tgeomap) {
            state.geomap_json = newValue;
        },
        Update_meta_data_json(state, newValue: Tmeta_geomapJson) {
            state.meta_data_json = newValue;
        },
        Update_select_PropertiesMark(state, newValue: TPropertiesMark) {
            state.select_PropertiesMark = newValue;
        },
        AUpdate_coordinat_click(state, newValue: TCoord) {
            state.coordinat_click = newValue;
        },
        Update_zoom_select(state, newValue: number) {
            state.zoom_select = newValue;
        },
        AUpdate_type_view(state, newValue: string) {
            state.type_view = newValue;
        },
        AUpdate_select_geomap_id(state, newValue: number) {
            state.select_geomap_id = newValue;
        },
        Update_url_geomap(state, newValue: string) {
            state.url_geomap = ParseUrlSrc(newValue);
        },
    },
    actions: {
        // Обновить координаты в фокуса
        Update_coordinat_click(
            {
                state, // то же, что и `store.state`, или локальный state при использовании модулей
                commit, // то же, что и `store.commit`
            },
            { coord, router, route }: { coord: TCoord; router: any; route: any }
        ) {
            commit("AUpdate_coordinat_click", coord);
            // Обновляем GET параметры в URL
            let query = clone(route.query);
            query[UrlGetParams.latitude] = coord.latitude;
            query[UrlGetParams.longitude] = coord.longitude;
            query[UrlGetParams.zoom] = state.zoom_select;
            query[UrlGetParams.type_view] = UrlGetParamsTypeView.main_map;
            router.push({ query: query });
        },
        Update_type_view(
            {
                commit, // то же, что и `store.commit`
            },
            {
                type_view,
                router,
                route,
            }: { type_view: string; router: any; route: any }
        ) {
            commit("AUpdate_type_view", type_view);
            // Обновляем GET параметры в URL
            let query = clone(route.query);
            query[UrlGetParams.type_view] = type_view;
            router.push({ query: query });
        },
        Update_select_geomap_id(
            {
                commit, // то же, что и `store.commit`
            },
            {
                geomap_id,
                router,
                route,
            }: { geomap_id: number; router: any; route: any }
        ) {
            commit("AUpdate_select_geomap_id", geomap_id);
            let query = clone(route.query);
            query[UrlGetParams.type_view] = geomap_id;
            router.push({ query: query });
        },
    },
    // Локальное пространство имен. Позволяет обращаться к мутации через `ИмяМодуляХранилища/ФункцияМутации`
    namespaced: true,
};
