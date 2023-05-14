<template>
    <div id="main_box">
        <!-- Всплывающий слой -->
        <div v-show="view_component" class="over_box">
            <OverBox @hidden_over_box="hidden_over_box" :view_component="view_component" />
        </div>
        <!-- Блок с картой -->
        <div class="up_box">
            <MapContainer ref="MapContainer" @onMarkerClick="HandleMarkerClick" @onEmptyMapClick="HandleEmptyMapClick" />
        </div>
        <!-- Блок с краткой информацией -->
        <div class="down_box">
            <!-- Кнопка для показания большей информации -->
            <div ref="d_show_map_detail" class="d_show_map_detail">
                <!-- Стрелка вверх.  -->
                <input class="show_map_detail" type="image" v-show="is_show_map_detail" ref="show_map_detail"
                    @click="ShowExtraFeaturesWindow" />
                <!-- Иконка для перехода в подробную информацию о месте -->
                <input class="show_map_detail" type="image" v-show="!is_show_map_detail" ref="show_map_detail_place"
                    @click="ShowPlaceDetailsInfo" />
            </div>
            <!-- Отображает координаты, на которые было совершено нажатие мышью -->
            <div class="map_coord_click">
                <input type="text" :value="coordinat_click" id="map_coord_click_input" placeholder="широта,долгота"
                    readonly />
            </div>
            <!-- Поверхностная информация о месте -->
            <div v-show="is_show_FacileFromMarker" class="map_facile_div">
                <FacileFromMarker ref="map_facile" />
            </div>
            <!-- Детальная информация о месте -->
            <!-- <div class="map_detail hidden"> -->
            <!-- Ввод координат, после расфокусировки с ввода, карта переместиться в указанные координаты -->
            <!-- <div class="map_set_coord"> -->
            <!-- <input ref="i_main_box_menu" type="text" placeholder="Найти: широта,долгота" -->
            <!-- @blur="setCoordinates($event.target.value)" /> -->
            <!-- </div> -->
        </div>
    </div>
</template>
<script lang="ts">
/*
Главный виджет которые имеет виджеты
- Карту (MapContainer)
- Информацию о выбранном мести
*/

import MapContainer from "@/components/MapContainer.vue";
import FacileFromMarker from "@/components/FacileFromMarker.vue";
import OverBox from "@/components/OverBox.vue";
import MapBrowserEvent from "ol/MapBrowserEvent";
import { ParseUrlSrc, ParseUrlBackend, clone, DownloadFromUrl, TFromUrl } from "@/helper";
import { UrlGetParams, UrlGetParamsTypeView, TCoord } from "@/interface";

// ФОТО
export const arrow_up = ParseUrlSrc("@/img/arrow_up.svg");
export const info_from_place = ParseUrlSrc("@/img/info_from_place.svg");
// URL для скачивания мета данных о geomap
export const geomap_list_from_channel_url = ParseUrlBackend(
    "@/api/v1/channel_geomap_place/"
);
// URL для скачивания What Todo
export const what_todo_url = ParseUrlBackend("@/api/v1/what_todo/");
// URL для скачивания Type Place
export const type_place_list_url = ParseUrlBackend("@/api/v1/type_place/");
// URL для создание нового места
export const place_url = ParseUrlBackend("@/api/v1/place/");
// URL для получения списка каналов
export const channel_geomap = ParseUrlBackend("@/api/v1/channel_geomap/");


export default {
    name: "MapApp",
    components: {
        MapContainer,
        FacileFromMarker,
        OverBox,
    },
    data() {
        return {
            // ------- Для OverBox
            // Какой компонент отображается в всплывающем окне
            view_component: <string>undefined,
            // Переключатели для отображения объектов в HTML
            is_show_FacileFromMarker: false,
            is_show_map_detail: true,
        };
    },
    async mounted() {
        // 0. Загружаем изображения
        this.$refs["show_map_detail"].src = arrow_up;
        this.$refs["show_map_detail_place"].src = info_from_place;
        // 1. Парсить URL и занести данные в Store
        await this.Mounted_ParseUrl();
        // 2. URL для получения списка мест в указном канале
        this.$store.commit(
            `geomap/Update_url_geomap`,
            ParseUrlSrc(geomap_list_from_channel_url) +
            this.$store.state.geomap.select_channel_geomap.id
        );
        // 3. Инициализировать карту
        this.$refs["MapContainer"]._initMap(
            this.$store.state.geomap.coordinat_click,
            this.$store.state.geomap.select_zoom,
            this.$store.state.geomap.url_geomap
        );
    },
    computed: {
        // Координаты фокусировки
        coordinat_click() {
            const c = <TCoord | undefined>(
                this.$store.state.geomap.coordinat_click
            );
            if (c) {
                return [c.latitude, c.longitude];
            }
            return [];
        },
    },
    methods: {
        // Сфокусироваться на указанных координатах
        setCoordinates(coord: string, IfSetMark = false) {
            this.$refs["MapContainer"].setCoordinates(
                this.$refs["MapContainer"]._parseCoordFromOpenstreetmap(coord),
                IfSetMark
            );
        },
        // Обработка нажатия на маркер
        HandleMarkerClick(PropertiesMark) {
            // Показать поверхностную информацию
            this.ShowPlaceFacileInfo();
        },
        // Нажатие на пустое место карты(без маркеров)
        HandleEmptyMapClick(evt: MapBrowserEvent<UIEvent>) {
            // Показываем кнопку(стрелка вверх) дистальной информации
            this.is_show_map_detail = true;
            // Скрываем  панель "Поверхностной информации"
            this.is_show_FacileFromMarker = false;
        },
        // Показать поверхностную информацию о выбранном месте
        ShowPlaceFacileInfo() {
            // Скрываем кнопку(стрелка вверх) детальной информации
            this.is_show_map_detail = false;
            // Показываем панель "Поверхностной информации"
            this.is_show_FacileFromMarker = true;
        },
        // Показать подробную информацию о месте
        ShowPlaceDetailsInfo() {
            // Показываем во всплывающем окне детальную информацию о месте
            this.view_component = "DetailFromPlace";
        },
        // Показать окно дополнительными возможностями
        ShowExtraFeaturesWindow() {
            this.view_component = "ExtraFeaturesWindow";
        },
        // Скрыть всплывающие окно
        hidden_over_box() {
            // Скрываем выплывающие окна
            this.view_component = undefined;
        },
        // --------------------
        async Mounted_ParseUrl() {
            /* Парсить URL и занести данные в Store */

            // 0. Текущие GET параметры в URL
            let query = clone(this.$route.query);
            // 1. Получить канал из URL
            const channel = parseInt(query["c"]);
            if (channel) {
                const channels: TFromUrl = await DownloadFromUrl(
                    channel_geomap + channel
                );
                if (channels.ok) {
                    const channels_json = channels.data;
                    this.$store.dispatch("geomap/Update_select_channel", {
                        channel: channels_json,
                        router: this.$router,
                        route: this.$route,
                    });
                }
                else {
                    console.error('Не удалось получить список каналов')
                }
            } else {
                console.log("Не указан ID канала");
                this.$router.push({ name: 'list_channels' });
                return
            }
            // 2. Получить масштаб карты из URL
            let zoom = parseInt(query["z"]);
            if (!zoom) {
                zoom = 16;
            }
            this.$store.commit(`geomap/Update_select_zoom`, zoom);
            // 3. Получить координаты для фокусировки

            this.$store.dispatch(`geomap/Update_coordinat_click`, {
                coord:
                    query[UrlGetParams.latitude] &&
                        query[UrlGetParams.longitude]
                        ? {
                            latitude: query[UrlGetParams.latitude],
                            longitude: query[UrlGetParams.longitude],
                        }
                        : {
                            latitude: this.$store.state.geomap.select_channel_geomap.default_coord_x,
                            longitude: this.$store.state.geomap.select_channel_geomap.default_coord_y,
                        },
                router: this.$router,
                route: this.$route,
            });
            // 4. Обновляем тип отображения
            this.$store.dispatch(`geomap/Update_type_view`, {
                type_view: query[UrlGetParams.type_view]
                    ? query[UrlGetParams.type_view]
                    : UrlGetParamsTypeView.main_map,
                router: this.$router,
                route: this.$route,
            });
            // 5. Обновляем  GET параметры в URL
            this.$router.push({ query: query });
        },
    },
};
</script>

<style lang="scss">
@import "@/gcolor.scss";

#main_box {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    height: 100%;
    width: 100%;
    display: flex;

    .up_box {
        flex-basis: 100%;
    }

    .down_box {
        position: absolute;
        left: 0px;
        bottom: 0px;
        width: 100%;
        display: flex;
        flex-direction: column;

        .d_show_map_detail {
            margin-bottom: 3px;
            text-align: end;

            .show_map_detail {
                border: none;
                width: 3rem;
                height: 3rem;
                position: relative;
                right: 4px;
            }
        }

        .map_coord_click,
        .map_set_coord {
            text-align: center;
            background-color: $ЦветФона;
            padding-top: 4px;

            input {
                font-size: medium;
                border-radius: 4px;
                width: 21em;
                height: 100%;
                text-align: center;
                background: $ЦветФонаПодсказки;
                color: $ЯркоеВыделение;
                border: none;
                outline: none;
            }
        }

        .map_set_coord {
            input {
                color: $ЯркоеВыделение2;
            }
        }

        .map_facile_div {
            background: $ЦветФона;
        }

        .map_detail {}
    }
}
</style>
