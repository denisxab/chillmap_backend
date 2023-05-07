<!-- Основная страница -->
<template>
    <div style="width: 100%; height: 100%">
        <!-- Карта -->
        <div ref="map-root" style="width: 100%; height: 100%"></div>
    </div>
</template>

<script lang="ts">
//  Импорт виджетов
import View from "ol/View";
import olMap from "ol/Map";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat, transform } from "ol/proj";
import BaseLayer from "ol/layer/Base";
import Collection from "ol/Collection";
// Импорт стилей для карты
import "ol/ol.css";
import { Point } from "ol/geom";
import Vector_source from "ol/source/Vector";
import Vector_layer from "ol/layer/Vector";
import Feature from "ol/Feature";
import Style from "ol/style/Style";
import Text from "ol/style/Text";
import Icon from "ol/style/Icon";
import { toSize } from "ol/size";
import Layer from "ol/layer/Layer";
import Fill from "ol/style/Fill";
import { DownloadFromUrl, ParseUrlSrc, TDownloadFromUrl } from "@/helper";
import Stroke from "ol/style/Stroke";
import MapEvent from "ol/MapEvent";
import MapBrowserEvent from "ol/MapBrowserEvent";
import { Tgeomap, TCoord, TPropertiesMark } from "@/interface";

// Картинка маркера по умолчанию
const imgPont = ParseUrlSrc("@/img/default_point.png");
// Картинка для маркера выбранных координат на карте
const imgSelect = ParseUrlSrc("@/img/select.png");

export default {
    emits: [
        // Нажатие на маркер
        "onMarkerClick",
        // Нажатие на карту(кроме нажатия на маркер)
        "onEmptyMapClick",
    ],
    data() {
        return {
            // Основной объект карты
            map: undefined,
            // Основной слой на карте
            mainLayer: new TileLayer({
                // https://openlayers.org/en/latest/apidoc/module-ol_layer_Tile-TileLayer.html
                // Имя класса для слоя
                className: "mainLayer",
                // Источник для этого слоя.
                source: new OSM(),
                // Предварительная загрузка фрагментов карты, чтобы не было серых квадратов при перемещение по карте
                preload: 4,
                // Этот видимый слой
                visible: true,
            }),
            // Слой на котором храниться координаты, на которые было совершено нажатие,
            // или если в кукую-то точку на карет было автоматическое перемещение.
            selectLayer: new Vector_layer({
                className: "selectLayer",
                source: new Vector_source(),
                style: new Style({
                    // Иконка маркера
                    image: new Icon({
                        // Ссылка на URL изображения
                        src: imgSelect,
                        // Масштаб изображения = по умолчанию [1,1]
                        scale: toSize([0.4, 0.4]),
                    }),
                }),
                visible: true,
            }),
            // Слой для маркеров на карте.
            markersLayer: new Vector_layer({
                // Имя класса
                className: "markersLayer",
                source: new Vector_source(),
                style: new Style({
                    // Иконка маркера
                    image: new Icon({
                        // Ссылка на URL изображения
                        src: imgPont,
                        // Масштаб изображения = по умолчанию [1,1]
                        scale: toSize([0.3, 0.3]),
                    }),
                }),
                visible: true,
            }),
            // Объект в котором будет храниться маркер, это нужно для того чтобы можно было удалять маркеры с прошлого нажатия
            coordinat_click_obj_mark: undefined,
        };
    },

    methods: {
        // Инициализировать карту. Используется такой вариант для того чтобы дождаться `async mounted`
        _initMap(
            default_coord: TCoord,
            default_zoom: number,
            default_url_geomap: string
        ) {
            // default_coord: Координаты на которые происходит фокусировки по умолчанию
            // default_zoom: Приближение карты по умолчанию
            // default_url_geomap: URL для скачивания geomap

            // Инициализация карты
            this.map = new olMap({
                // HTML объект в который вставиться карта
                target: this.$refs["map-root"],
                // Список слоев на карте
                layers: [
                    // Основной слой на карте
                    this.mainLayer,
                    // Слой на кортом храниться текущие нажатые координаты
                    this.selectLayer,
                ],
                // Начальные положение на карте
                view: new View({
                    // Приближение карты по умолчанию
                    zoom: default_zoom,
                    // Положение по умолчанию
                    center: fromLonLat([
                        default_coord.longitude,
                        default_coord.latitude,
                    ]),
                    // Установите, должен ли вид разрешать промежуточные уровни масштабирования.
                    constrainResolution: true,
                    // проекция. По умолчанию используется Сферический Меркатор.
                    projection: "EPSG:3857",
                }),
            });
            // Поставить маркер на сфокусированные координаты
            this.setSelectMarker(default_coord);
            // Добавляем на карту слой с маркерами
            this.map.addLayer(this.markersLayer);
            // Про типы обработчиков событий https://gis.stackexchange.com/questions/252946/what-are-the-possible-listeners-and-event-types-for-an-openlayers-map-ol-map
            // Добавить обработчик событий на нажатие на карту
            this.map.on("click", this.HandleClickMap); // MapBrowserEvent<UIEvent>
            // Добавить обработчик передвижения мыши по карте
            this.map.on("pointermove", this.HandlePointermove); // MapBrowserEvent
            // Обработка изменение маштака карты
            this.map.on("moveend", this.HandleZoom); // MapEvent
            // Скачиваем и обновляем geomap
            this.updateSelectGeomap(default_url_geomap);
            /////////////////// Тестовый маркер
            // this.setMarkers({ longitude: 30.1734, latitude: 59.8587 });
            // this.setMarkers({ longitude: 30.1734, latitude: 59.8588 }, undefined, {
            //     imgUrl: imgPont2,
            //     imgSize: [0.4, 0.4],
            // });
            ///////////////////
        },
        // ----------- Основные функции для работы с Openlayers -------------
        // Приблизить карту
        ZoomMap() {
            this.$store.commit(
                `geomap/Update_zoom_select`,
                this.$store.state.geomap.zoom_select + 1
            );
        },
        // отдалить карту
        UnZoomMap() {
            this.$store.commit(
                `geomap/Update_zoom_select`,
                this.$store.state.geomap.zoom_select - 1
            );
        },
        // Сфокусировать карту в указанные координаты
        setCoordinates(coord: TCoord | undefined, IfSetMark = false) {
            // coord: Координаты куда сфокусироваться
            // IfSetMark: True=Установит маркер в указанные координаты
            if (coord) {
                this.view_select.setCenter(
                    fromLonLat([coord.longitude, coord.latitude])
                );
                if (IfSetMark) {
                    this.setSelectMarker(coord);
                }
            }
        },
        // Установить маркер в указанные координаты на карте
        setMarkers(
            coord: TCoord | undefined,
            propsFromFeature: { [x: string]: any } = undefined,
            {
                imgUrl = <string>undefined,
                imgSize = <[number, number]>[1, 1],
                labelText = <string>"12:Пивная",
            } = {}
        ) {
            // coord: Координаты куда поставить маркер
            // imgUrl: Путь к изображению маркера
            // sizeImg: Масштаб для маркера. [1,1] = Исходный размер изображения
            // propsFromFeature: Параметры которые сохраняться в маркер, их можно будет получить через - `marker.getProperties()['ИмяКлюча'];`
            // labelText16size: Название места. Максимальная длинна 16 символов
            /*
                this.setMarkers({ longitude: 30.1734, latitude: 59.8587 });
            */
            if (coord) {
                // Создаем маркер
                let marker = new Feature({
                    geometry: new Point(
                        fromLonLat([coord.longitude, coord.latitude])
                    ),
                });
                if (imgUrl) {
                    // Если передано изображение, то отображаем его, а не то что задано по умолчанию.
                    marker.setStyle(
                        new Style({
                            // Иконка маркера
                            image: new Icon({
                                // Ссылка на URL изображения
                                src: imgUrl,
                                // Масштаб изображения = по умолчанию [1,1]
                                scale: toSize(imgSize),
                            }),
                            // Стили для текста https://openlayers.org/en/latest/apidoc/module-ol_style_Text-Text.html
                            text: new Text({
                                // Текст
                                text: labelText,
                                // Размер текста
                                scale: [1.3, 1.3],
                                // Стиль текста
                                // font: "10px sans-serif bold",
                                // Отступ с верху
                                offsetY: 28,
                                // Цвет фона
                                // backgroundFill: new Fill({ color: "#ebcb8b" }),
                                // Цвет обводки текста
                                stroke: new Stroke({
                                    color: "#fff",
                                    width: 3,
                                }),
                                placement: "line",
                            }),
                        })
                    );
                }
                if (propsFromFeature) {
                    // Сохранить параметры в маркер
                    /*
                    Получить параметры из маркера

                    >>> marker.getProperties()['ИмяКлюча'];
                    */
                    marker.setProperties(propsFromFeature);
                }
                // Добавляем его на карту
                this.markersLayer.getSource().addFeature(marker);
            }
        },
        // Установить маркер на место в которые было совершено нажатие
        setSelectMarker(coord: TCoord | undefined) {
            // longitude: долгота
            // latitude: широта
            /*
                this.setSelectMarker({ longitude: 30.1734, latitude: 59.8587 });
            */
            if (coord) {
                // Удаляем маркер с прошлого нажатия
                this.selectLayer
                    .getSource()
                    .removeFeature(this.coordinat_click_obj_mark);
                // Создаем маркер
                var marker = new Feature(
                    new Point(fromLonLat([coord.longitude, coord.latitude]))
                );
                // Обновляем маркер нажатия на новый
                this.coordinat_click_obj_mark = marker;
                // Добавляем маркер на карту
                this.selectLayer.getSource().addFeature(marker);
            }
        },
        // Загрузить geomap_ИмяТочкиРадиусов.json и обновить все маркеры мест на карте, в соответствие с этим файлом
        async updateSelectGeomap(url_download: string) {
            const geomap: TDownloadFromUrl = await DownloadFromUrl(url_download);
            if (geomap.ok) {
                // TODO: сделать чтобы работала пагинация
                const geomap_json: Tgeomap[] = JSON.parse(await geomap.text).results;
                // Убираем с карты маркеры от прошлых места
                this.ClearMarkers(this.markersLayer);
                // Заносим Geomap в глобальное хранилище
                this.$store.commit("geomap/Update_geomap_json", geomap_json);
                // Отображаем места на карте
                this.ShowPlaceFromExternal(
                    this.markersLayer,
                    this.$store.state.geomap.geomap_json
                );
            } else {
                console.error("Ошибка: Ответ geomap пустой");
            }
        },
        // Отчистить указный слой от всех маркеров
        ClearMarkers(layer: Vector_layer<Vector_source>) {
            layer.getSource().clear();
        },
        // Отобразить места на карте из формата `Tgeomap`
        ShowPlaceFromExternal(layer: Layer, self_geomap: Tgeomap[]) {
            // layer: На какой слой добавить маркеры.
            // self_geomap: Объект с данными имеющий координаты и стили для маркеров.

            // 1. Показать слой
            layer.setVisible(true);

            self_geomap.forEach(element => {
                element.group_place_obj
                
            });

            // 2. Парсим список координат
            for (const [name_group, value_group] of Object.entries(
                self_geomap
            )) {
                // 2.1 Получаем стили для текущей группы
                let style = {};
                const style_geom = self_geomap.geom_place_style[name_group];
                if (style_geom) {
                    style = {
                        imgUrl: ParseUrlSrc(style_geom.img_url),
                        imgSize: style_geom.img_size,
                    };
                }
                // 2.2 Перебираем список координат для текущей группы
                for (const [key_coord, value_place] of Object.entries(
                    value_group
                )) {
                    const coord = this._parseCoordFromOpenstreetmap(key_coord);
                    // Формируем краткую информацию о месте. Рейтинг:Имя
                    style["labelText"] = `${
                        // Максимум 12 баллов
                        value_place.rating % 13
                        }:${
                        // Максимальная длинна названия 16 символов
                        value_place.simpl_name.substring(0, 16)
                        }`;
                    // Своиства которы будут храниться в маркере
                    let PropertiesMark = <TPropertiesMark>value_place;
                    PropertiesMark["name_marker"] = style_geom.name_marker;
                    PropertiesMark["coord"] = [coord.latitude, coord.longitude];
                    // 2.2.1 Устанавливаем маркеры
                    this.setMarkers(coord, PropertiesMark, style);
                }
            }
        },
        //  ---------- Обработчики событий на карте  ------------------ //

        // Проверка пересечения события с маркером
        _CheckIntersectionsMarker(evt: MapBrowserEvent<UIEvent>) {
            // return: True=Есть пересечение с маркером. False=Нет пересечения с маркером
            let res = false;
            // Обнаружьте объекты, которые пересекают пиксель в окне просмотра, и выполните обратный вызов с каждой пересекающейся функцией
            this.map.forEachFeatureAtPixel(
                // Пиксили в которых искать пересечение с объектом
                evt.pixel,
                // Обработка пересечения с маркером
                (feat: Feature, layer: BaseLayer) => {
                    // Если пересечение с элементом у которого className="markersLayer" (слой с маркерами)
                    if (layer.getClassName() == "markersLayer") {
                        this.HandleMarkerHover(evt, feat);
                        res = true;
                    }
                }
            );
            return res;
        },
        // Обработки нажатий на карту
        HandleClickMap(evt: MapBrowserEvent<UIEvent>): any {
            // Если было пересечение с маркером то, не изменяем положение курсора на карте
            if (this._CheckIntersectionsMarker(evt)) {
                return null;
            }
            // Конвертировать координаты в широту и долготу
            const coord = transform(
                evt.coordinate,
                "EPSG:3857",
                "EPSG:4326"
            ).reverse();
            // Сохраняем нажатые координаты в глобальное хранилище
            this.$store.dispatch(`geomap/Update_coordinat_click`, {
                coord: {
                    latitude: coord[0],
                    longitude: coord[1],
                },
                router: this.$router,
                route: this.$route,
            });
            if (coord) {
                // Устанавливаем маркер в координаты нажатия
                this.setSelectMarker(
                    this._parseCoordFromOpenstreetmap(coord.toString())
                );
            }
            console.log("Нажатие по карте, в координаты: ", coord);
            this.$emit("onEmptyMapClick", evt);
        },
        // Обработчик передвижения мыши по карте
        HandlePointermove(evt: MapBrowserEvent<UIEvent>) {
            // Проверить пересечения с маркером
            this._CheckIntersectionsMarker(evt);
        },
        // Обработка наведения миши на маркер
        HandleMarkerHover(evt: MapBrowserEvent<UIEvent>, feat: Feature) {
            // Если это наведение на маркер
            if (evt.type == "pointermove") {
                console.debug("Наведение на маркер");
            }
            // Если это нажатие на маркер
            if (evt.type == "click") {
                this.HandleMarkerClick(feat);
            }
        },
        // Обработка нажатия на маркер
        HandleMarkerClick(feat: Feature) {
            // Кастомные свойства у нажатого маркера
            const PropertiesMark = <TPropertiesMark>feat.getProperties();
            // Сохраняем в ГХ текущие выбранное место;
            this.$store.commit(
                `geomap/Update_select_PropertiesMark`,
                PropertiesMark
            );
            // Координаты фокусировки равны = координатам нажатого места
            this.$store.dispatch(`geomap/Update_coordinat_click`, {
                coord: {
                    latitude: PropertiesMark.coord[0],
                    longitude: PropertiesMark.coord[1],
                },
                router: this.$router,
                route: this.$route,
            });
            console.log("Нажатие на маркер", PropertiesMark);
            // Вызываем событие нажатия на маркер
            this.$emit("onMarkerClick", PropertiesMark);
        },
        // Обработка изменение масштаба карты
        HandleZoom(evt: MapEvent) {
            this.$store.commit(
                `geomap/Update_zoom_select`,
                this.view_select.values_.zoom
            );
        },
        //-------------------------------------------------------------

        // ----- Утилиты -----------------------------
        // Конвертировать строку координат из https://www.openstreetmap.org/
        _parseCoordFromOpenstreetmap(str_coord: string): TCoord | undefined {
            if (str_coord != "") {
                const l = str_coord.split(",").reverse();
                if (l.length == 2) {
                    return {
                        longitude: parseFloat(l[0]),
                        latitude: parseFloat(l[1]),
                    };
                }
            } else {
                console.warn("Вы не указали координаты");
            }
        },
    },
    computed: {
        // View у карты
        view_select(): View {
            return this.map.getView();
        },
        // Получить все слои на карте
        layers_select(): Collection<BaseLayer> {
            return this.map.getLayers();
        },
    },
};
</script>
