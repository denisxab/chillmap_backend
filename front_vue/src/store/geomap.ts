import {
    TCoord,
    TGeomap,
    Tchannel_geomapJson,
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
            geomap_json: <TGeomap[]>{},
            // Все каналы данные
            channel_geomap_json: <Tchannel_geomapJson>{},
            // Текущие выбранное место
            select_PropertiesMark: <TPropertiesMark>undefined,
            // Координаты на которое совершено нажатие, или фокусировка
            coordinat_click: <TCoord>{
                latitude: 59.859292472503114,
                longitude: 30.169246265131953,
            },
            // Текущие приближение карты
            select_zoom: <number>16,
            // Режим просмотра
            type_view: <string>UrlGetParamsTypeView.main_map,
            // Текущий id канала для просмотра
            select_channel_geomap: <number>1,
            // Ссылка для скачивания geomap
            url_geomap: <string>undefined,
        };
    },
    mutations: {
        // ----------------
        AUpdate_select_channel(state, newValue: number) {
            state.select_channel_geomap = newValue;
        },
        Update_select_zoom(state, newValue: number) {
            state.select_zoom = newValue;
        },
        AUpdate_coordinat_click(state, newValue: TCoord) {
            state.coordinat_click = newValue;
        },
        AUpdate_type_view(state, newValue: string) {
            state.type_view = newValue;
        },
        // ----------------
        Update_geomap_json(state, newValue: TGeomap[]) {
            state.geomap_json = newValue;
        },
        Update_channel_geomap_json(state, newValue: Tchannel_geomapJson) {
            state.channel_geomap_json = newValue;
        },
        AUpdate_select_PropertiesMark(state, newValue: TPropertiesMark) {
            state.select_PropertiesMark = newValue;
        },
        Update_url_geomap(state, newValue: string) {
            state.url_geomap = ParseUrlSrc(newValue);
        }
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
            query[UrlGetParams.zoom] = state.select_zoom;
            query[UrlGetParams.type_view] = UrlGetParamsTypeView.main_map;
            if (state.select_PropertiesMark) {
                query[UrlGetParams.mark] = state.select_PropertiesMark.id;
            }
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
        Update_select_channel(
            {
                commit, // то же, что и `store.commit`
            },
            {
                channel,
                router,
                route,
            }: { channel: number; router: any; route: any }
        ) {
            commit("AUpdate_select_channel", channel);
            let query = clone(route.query);
            query[UrlGetParams.channel] = channel;
            router.push({ query: query });
        },
        Update_select_PropertiesMark({
            commit, // то же, что и `store.commit`
        },
            {
                mark,
                router,
                route,
            }: { mark: TPropertiesMark; router: any; route: any }) {
            commit("AUpdate_select_PropertiesMark", mark);
            let query = clone(route.query);
            query[UrlGetParams.mark] = mark.id;
            router.push({ query: query });
        },
    },
    // Локальное пространство имен. Позволяет обращаться к мутации через `ИмяМодуляХранилища/ФункцияМутации`
    namespaced: true,
};
