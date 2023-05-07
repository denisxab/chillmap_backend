<template>
    <div id="main_box">
        <!-- Всплывающий слой -->
        <div v-show="view_component" class="over_box">
            <OverBox @hidden_over_box="hidden_over_box" :view_component="view_component" />
        </div>
        <!-- Блок с картой -->
        <div class="up_box">
            <MapContainer
                ref="MapContainer"
                @onMarkerClick="HandleMarkerClick"
                @onEmptyMapClick="HandleEmptyMapClick"
            />
        </div>
        <!-- Блок с краткой информацией -->
        <div class="down_box">
            <!-- Кнопка для показания большей информации -->
            <div ref="d_show_map_detail" class="d_show_map_detail">
                <!-- Стрелка вверх.  -->
                <input class="show_map_detail" type="image" ref="show_map_detail" v-show="is_show_map_detail" />
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
            <!-- <div class="map_set_coord">
                    <input
                        ref="i_main_box_menu"
                        type="text"
                        placeholder="Найти: широта,долгота"
                        @blur="setCoordinates($event.target.value)"
                    />
                </div> -->
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
import { DownloadFromUrl, ParseUrlSrc, ParseUrlBackend, TDownloadFromUrl, clone } from "@/helper";
import {
    TPropertiesMark,
    UrlGetParams,
    UrlGetParamsTypeView,
    Tmeta_geomapJson,
    Tmeta_geomapJson_names_radius,
    TCoord,
} from "@/interface";

// ФОТО
export const arrow_up = ParseUrlSrc("@/img/arrow_up.svg");
const info_from_place = ParseUrlSrc("@/img/info_from_place.svg");
// URL для скачивания мета данных о geomap
const meta_geomap_url = ParseUrlBackend("@/api/v1/meta_geomap/");
const geomap_list_from_meta_url = ParseUrlBackend("@/api/v1/place/?meta_geomap=");

export default {
    name: "MapApp",
    components: { MapContainer, FacileFromMarker, OverBox },
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
    methods: {
        // Сфокусироваться на указанных координатах
        setCoordinates(coord: string, IfSetMark = false) {
            this.$refs["MapContainer"].setCoordinates(
                this.$refs["MapContainer"]._parseCoordFromOpenstreetmap(coord),
                IfSetMark
            );
        },
        // Обработка нажатия на маркер
        HandleMarkerClick(PropertiesMark: TPropertiesMark) {
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
        // Скрыть всплывающие окно
        hidden_over_box() {
            // Скрываем выплывающие окна
            this.view_component = undefined;
        },
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
    async mounted() {
        //
        // Загружаем изображения
        //
        this.$refs["show_map_detail"].src = arrow_up;
        this.$refs["show_map_detail_place"].src = info_from_place;


        let default_url_geomap = null
        //
        //
        // 1. Скачиваем мета данные
        const meta_geomap: TDownloadFromUrl = await DownloadFromUrl(
            meta_geomap_url
        );
        let meta_geomap_json = <Tmeta_geomapJson>{};
        if (meta_geomap.ok) {
            meta_geomap_json = JSON.parse(await meta_geomap.text);
            // Сохраняем мета данные в store
            this.$store.commit(`geomap/Update_meta_data_json`, meta_geomap_json.results);
            // TODO: Сделать не выбор первых, а как то умнее
            // 2. Получаем список мест в группе (* первый попавшейся)
            default_url_geomap = geomap_list_from_meta_url + meta_geomap_json.results[0].id
        } else {
            console.error("Ошибка: Мета данные пустые");
        }
        //
        // Текущие GET параметры в URL
        //
        let query = clone(this.$route.query);
        //
        // Переопределяем масштаб карты, если жто указана в GET параметре
        //
        const zoom = parseInt(query["z"]);
        if (zoom) {
            this.$store.commit(`geomap/Update_zoom_select`, zoom);
        }
        //
        // Обновляем координаты для фокусировки
        //
        this.$store.dispatch(`geomap/Update_coordinat_click`, {
            // Фокусируемся на координатах которые были переданы в GET параметрах
            coord:
                query[UrlGetParams.latitude] && query[UrlGetParams.longitude]
                    ? {
                        latitude: query[UrlGetParams.latitude],
                        longitude: query[UrlGetParams.longitude],
                    }
                    : this.$store.state.geomap.coordinat_click,
            router: this.$router,
            route: this.$route,
        });
        //
        // Берем ID geomap из GET параметров если есть
        //
        // Ссылка на радиус интересных мест по умолчанию
        // let default_url_geomap = undefined;
        // let id_geomap = query[UrlGetParams.geomap];
        // // Пробуем взять geomap из GET параметра
        // if (id_geomap) {
        //     // Путь к файлу с geomap.json
        //     default_url_geomap =
        //         meta_geomap_json.names_radius[id_geomap].name_path;
        // }
        // Иначе, по умолчанию берем первый geomap из мета данных
        // else {
        //     // TODO: Исправить
        //     const geomap = <[string, Tmeta_geomapJson_names_radius]>(
        //         Object.entries(meta_geomap_json.names_radius)[0]
        //     );
        //     // Путь к файлу с geomap.json
        //     default_url_geomap = geomap[1].name_path;
        //     // Обновляем выделенную группу
        //     this.$store.dispatch(`geomap/Update_select_geomap_id`, {
        //         // Фокусируемся на координатах которые были переданы в GET параметрах
        //         geomap_id: geomap[0],
        //         router: this.$router,
        //         route: this.$route,
        //     });
        // }
        this.$store.commit(`geomap/Update_url_geomap`, default_url_geomap);
        //
        // Обновляем  GET параметры в URL
        //
        this.$router.push({ query: query });
        //
        // Обновляем тип отображения
        //
        this.$store.dispatch(`geomap/Update_type_view`, {
            type_view: query[UrlGetParams.type_view]
                ? query[UrlGetParams.type_view]
                : UrlGetParamsTypeView.main_map,
            router: this.$router,
            route: this.$route,
        });
        //
        // Инициализировать карту
        //
        this.$refs["MapContainer"]._initMap(
            this.$store.state.geomap.coordinat_click,
            this.$store.state.geomap.zoom_select,
            ParseUrlSrc(default_url_geomap)
        );
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
