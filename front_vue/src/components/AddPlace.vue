<!-- Это компонент для создание нового места в БД -->
<template>
    <div class="box_extra">
        <label class="row">
            <div class="label">* Короткое имя:</div>
            <input v-model="shortName" />
        </label>
        <label class="row">
            <div class="label">* Рейтинг места:</div>
            <input v-model="rating" type="number" min="1" max="5" />
        </label>
        <label class="row">
            <div class="label">* What to do:</div>
            <select v-model="todo" multiple class="todo">
                <option v-for="option in todoOptions" :value="option">
                    {{ option.todo }}
                </option>
            </select>
        </label>
        <label class="row">
            <div class="label">* Type place:</div>
            <select v-model="typePlace">
                <option v-for="option in typePlaceOptions" :value="option">
                    {{ option.name }}
                </option>
            </select>
        </label>
        <VButton class="send_bt" value="Отправить" @clickBt="create_geomap" />
        <input
            ref="hidden_elm"
            class="hidden_elm"
            type="image"
            @click="hidden_elm" />
    </div>
</template>

<script lang="ts">
import { DownloadFromUrl, ParseUrlSrc, PostJsonFromUrl } from "@/helper";
import { TCoord, TTypePlaceObj, TWhatTodoObj } from "@/interface";
import {
    arrow_up,
    place_url,
    type_place_list_url,
    what_todo_url,
} from "@/pages/MapApp.vue";
import VButton from "@/stylecomponents/VButton.vue";

export default {
    emits: ["hidden_elm", "hiddenOverBox"],
    components: { VButton },
    mounted() {
        this.$refs["hidden_elm"].src = arrow_up;
        this.show();
    },
    data() {
        return {
            shortName: "",
            rating: 1,
            todo: [] as TWhatTodoObj[],
            typePlace: {} as TTypePlaceObj,
            todoOptions: [] as TWhatTodoObj[],
            typePlaceOptions: [] as TTypePlaceObj[],
        };
    },
    methods: {
        hidden_elm() {
            this.$emit("hidden_elm");
        },
        async create_geomap() {
            console.log("Отправка: создание нового места");
            const coord: TCoord = this.$store.state.geomap.coordinat_click;
            console.log(this.$refs);
            const req = {
                cord_x: coord.latitude,
                cord_y: coord.longitude,
                simpl_name: this.shortName,
                rating: this.rating,
                address: "",
                channel_geomap:
                    this.$store.state.geomap.select_channel_geomap.id,
                what_todo: this.todo.map((element) => element.id),
                type_place: this.typePlace.id,
            };
            const res = await PostJsonFromUrl(place_url, req);
            if (res.ok) {
                alert("Успешное создание нового места");
                this.hidden_elm();
                this.$emit("hiddenOverBox");
                // Если произошло успешное создание,
                // 1. TODO: Добавляем маркер на карту
                const settings_type_place =
                    this.$store.state.geomap.settings_type_place;
                const element = JSON.parse(res.data);
                const item = element.type_place;
                const img_url = settings_type_place[item].img_url;
                const img_size = [
                    settings_type_place[item].img_size_w,
                    settings_type_place[item].img_size_h,
                ];
                const style = {
                    imgUrl: ParseUrlSrc(img_url),
                    imgSize: img_size,
                };
                // Формируем краткую информацию о месте. Рейтинг:Имя
                style["labelText"] = `${
                    // Максимум 12 баллов
                    element.rating % 13
                }:${
                    // Максимальная длинна названия 16 символов
                    element.simpl_name.substring(0, 16)
                }`;
                const coord =
                    this.$store.state.geomap.RefMapContainer._parseCoordFromOpenstreetmap(
                        `${element.cord_x},${element.cord_y}`
                    );
                // Своиства которы будут храниться в маркере
                let PropertiesMark = element;
                PropertiesMark["name_marker"] = settings_type_place[item].name;
                PropertiesMark["coord"] = [coord.latitude, coord.longitude];
                // 2.2.1 Устанавливаем маркеры
                this.$store.state.geomap.RefMapContainer.setMarkers(
                    coord,
                    PropertiesMark,
                    style
                );
                // 2. Переходим на карту
                this.$router.push({
                    name: "main_map",
                    query: this.$route.query,
                });
            } else {
                alert(`Ошибка создания нового места: ${res.data}`);
            }
        },

        async show() {
            const [todoOptions, typePlaceOptions] = await Promise.all([
                DownloadFromUrl(what_todo_url),
                DownloadFromUrl(type_place_list_url),
            ]);

            if (todoOptions.ok) {
                this.todoOptions = todoOptions.data as TWhatTodoObj[];
            }

            if (typePlaceOptions.ok) {
                this.typePlaceOptions =
                    typePlaceOptions.data as TTypePlaceObj[];
            }

            this.typePlace = this.typePlaceOptions[0];
        },
    },
};
</script>

<style lang="scss" scoped>
@import "@/gcolor.scss";

.hidden_elm {
    -webkit-transform: rotate(270deg);
    -moz-transform: rotate(270deg);
    -o-transform: rotate(270deg);
    -ms-transform: rotate(270deg);
    transform: rotate(270deg);
    width: 5rem;
}

.box_extra {
    display: flex;
    flex-direction: column;
    width: 100%;
    color: $БазовыйЦветТекста;

    .row {
        box-shadow: 0px 0px 0.1rem 0.1rem $ЦветФонаВсплывающегоОкна;
        border-radius: 0.2rem;
        margin-bottom: 0.8rem;
        padding: 1rem;
        font-size: 1rem;
        text-align: left;
        flex-direction: row;

        &:hover {
            background: $ЦветФонаВсплывающегоОкна;
        }

        .label {
            margin-right: 0.5rem;
            width: 8rem;
            text-align: right;
            font-weight: bold;
            display: inline;
        }

        input,
        select {
            flex: 1;
            margin-left: 0.5rem;
            width: 100%;
            color: $БазовыйЦветТекста;
            background: $ЦветФонаВсплывающегоОкна;
        }

        .todo {
            height: 6rem;
        }
    }

    .send_bt {
        margin-bottom: 0.8rem;
        font-size: 1.3rem;

        &:hover {
            background: $ЦветФонаВсплывающегоОкна;
        }

        background: transparent;
        box-shadow: 0px 0px 0.1rem 0.1rem $ЦветФонаВсплывающегоОкна;
    }
}
</style>
