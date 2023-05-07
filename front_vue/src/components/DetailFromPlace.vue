<!-- Компонент для отображения детальная информация о месте -->
<template>
    <div class="box">
        <!-- Информация вв иде ключ значения -->
        <div class="row" v-for="(item, index) in view_list" :key="index">
            <div class="title">{{ item.title }}</div>
            <div class="view_list_data" v-for="(item2, index2) in item.data" :key="index2">
                <div class="name" v-if="item2.name">{{ item2.name }}</div>
                <div class="value">
                    <div class="list" v-if="typeof item2.value == 'object'">
                        <ParamsList :params_list="item2.value" />
                    </div>
                    <a target="_blank" :href="item2.value" v-else-if="
                        typeof item2.value == 'string' &&
                        item2.value.includes('://')
                    ">{{ item2.value }}</a>
                    <span v-else>
                        {{ item2.value }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import {
    EAverageCostVisit,
    EAveragePopulation,
    TPropertiesMark,
    Tpublic_place_details,
    TInternetСontacts,
} from "@/interface";
import {
    DownloadFromUrl,
    ParseUrlSrc,
    TDownloadFromUrl,
    whattodoIdFromName,
} from "@/helper";
import ParamsList from "@/components/ParamsList.vue";

// Формирует URL для скачивания ppd файла, по указному id места
export function template_download_ppd_file(id: number) {
    return ParseUrlSrc(`@/public_place_details/ppd_${id}.json`);
}
export interface Tview_list_item {
    // Имя группы
    title: string;
    // Данные у жой группы
    data: {
        // Имя параметра
        name?: string;
        // Значение параметра
        value: string | number | string[];
    }[];
}

function Def_InternetСontacts() {
    return {
        phones: undefined,
        website: undefined,
        tg: undefined,
        vk: undefined,
        any_social: undefined,
        yandex_map: undefined,
        any_link: undefined,
    };
}

export default {
    // Компоненты
    components: { ParamsList },
    // Переменные
    data() {
        return {
            //-- Из поверхностных данных
            name_marker: <string>undefined,
            rating: <number>undefined,
            simpl_name: <string>undefined,
            whattodo: <number[]>undefined,
            address: <string>undefined,
            //-- Из внешнего файла
            // Средняя людность:
            AveragePopulation: <string>undefined,
            // Средняя стоимость посещения.
            AverageCostVisit: <string>undefined,
            // У скольких пользователей, это место добавлено в избранные
            FavoritesCountMore: <number>undefined,
            // Это место в интернете
            InternetСontacts: <TInternetСontacts>Def_InternetСontacts(),
        };
    },
    // Методы
    methods: {
        // Функция для обновления данных в компоненте, она асинхронна потому что скачивает файл с подробными данными о месте
        async updateData(props: TPropertiesMark) {
            // Отчистить прошлые значения подробных данных
            this.clear_ppd();
            // Получаем новые подробные данные о месте
            // TODO: Переделать
            // const ppd_file: TDownloadFromUrl = await DownloadFromUrl(
            //     template_download_ppd_file(props.id)
            // );
            // if (ppd_file.ok) {
            //     // Распарсить подробные данные, и сохранить значения по нужным переменным
            //     this.parse_ppd(JSON.parse(await ppd_file.text));
            // } else {
            //     console.error("Ошибка: ppd файл пустой !");
            // }
        },
        // Распарсить подробные данные о месте, и записать их в нужные переменные
        parse_ppd(ppd: Tpublic_place_details) {
            this.AveragePopulation = EAveragePopulation[ppd.AveragePopulation];
            this.AverageCostVisit = `${ppd.AverageCostVisit.value} ${EAverageCostVisit[ppd.AverageCostVisit.currency]
                }`;
            this.InternetСontacts = ppd.InternetСontacts;
            this.FavoritesCountMore = `более ${ppd.FavoritesCountMore}`;
        },
        // Отчистить переменные которые были заполнены из подробных данных
        clear_ppd() {
            this.AveragePopulation = undefined;
            this.AverageCostVisit = undefined;
            this.InternetСontacts = Def_InternetСontacts();
            this.FavoritesCountMore = undefined;
        },
    },
    watch: {
        props_component: {
            handler(newValue: TPropertiesMark) {
                // Эти данные берутся из поверхностной информации
                this.name_marker = newValue.name_marker;
                this.rating = newValue.rating;
                this.simpl_name = newValue.simpl_name;
                this.address = newValue.address;
                this.whattodo = whattodoIdFromName(
                    newValue,
                    this.$store.state.geomap.geomap_json.geom_whattodo_det
                );
                // Получаем подробные данные о месте
                this.updateData(newValue);
            },
            deep: true,
        },
    },
    computed: {
        // Отслеживание изменений выбранного маркера
        props_component() {
            return this.$store.state.geomap.select_PropertiesMark;
        },
        // Формируем список который будет отображаться в HTML
        view_list(): Tview_list_item[] {
            return [
                {
                    title: "Общая информация",
                    data: [
                        {
                            name: "Тип маркера",
                            value: this.name_marker,
                        },
                        {
                            name: "Рейтинг",
                            value: this.rating,
                        },
                        {
                            name: "Название",
                            value: this.simpl_name,
                        },
                        {
                            name: "Адрес",
                            value: this.address,
                        },
                        {
                            name: "Средняя людность",
                            value: this.AveragePopulation,
                        },
                        {
                            name: "Средняя стоимость посещения",
                            value: this.AverageCostVisit,
                        },
                        {
                            name: "В избранных",
                            value: this.FavoritesCountMore,
                        },
                    ],
                },
                {
                    title: "Чем тут можно заняться",
                    data: [
                        {
                            value: this.whattodo,
                        },
                    ],
                },
                {
                    title: "Это место в интернете",
                    data: [
                        { name: "phones", value: this.InternetСontacts.phones },
                        {
                            name: "website",
                            value: this.InternetСontacts.website,
                        },
                        { name: "tg", value: this.InternetСontacts.tg },
                        { name: "vk", value: this.InternetСontacts.vk },
                        {
                            name: "any_social",
                            value: this.InternetСontacts.any_social,
                        },
                        {
                            name: "yandex_map",
                            value: this.InternetСontacts.yandex_map,
                        },
                        {
                            name: "any_link",
                            value: this.InternetСontacts.any_link,
                        },
                    ],
                },
            ];
        },
    },
};
</script>
<style lang="scss" scoped>
@import "@/gcolor.scss";

.box {
    margin: 0.3rem;
    display: flex;
    flex-direction: column;

    .row {
        box-shadow: 0px 0px 2rem 0.7rem $ЦветФонаВсплывающегоОкна;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        padding: 0.3rem;
        overflow: hidden;

        .title {
            color: $h_color;
            text-align: center;
            margin-top: 0.2rem;
            margin-bottom: 0.2rem;
        }

        .view_list_data {
            display: flex;
            flex-direction: row;
            margin-bottom: 0.2rem;
            padding: 0.1rem;

            .name {
                color: $h_color;

                &::after {
                    content: ":";
                }

                //
                padding-right: 0.3rem;
                //  Запрет выделения текста
                -webkit-touch-callout: none;
                -webkit-user-select: none;
                -khtml-user-select: none;
                -moz-user-select: none;
                -ms-user-select: none;
                user-select: none;
                // Текст по центру
                position: relative;
                top: 0;
                bottom: 0;
                margin: auto 0;
            }

            .value {
                overflow: auto;
            }
        }
    }

    a {

        /*
        Псевдокласс	Описание
        a:link	Определяет стиль для обычной не посещенной ссылки.
        a:visited	Определяет стиль для посещенной ссылки.
        a:active	Определяет стиль для активной ссылки. Активной ссылка становится при нажатии на нее.
        a:hover	Определяет стиль для ссылки при наведении на нее мышью.
        */
        &:link {}

        &:visited {}

        &:focus {}

        &:hover {}

        &:active {}

        //  Убрать подчёркивание ссылки
        text-decoration: none;
        color: $БазовыйЦветТекста;
    }
}
</style>
