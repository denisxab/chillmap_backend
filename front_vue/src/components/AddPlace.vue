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
import { DownloadFromUrl, PostJsonFromUrl } from "@/helper";
import { TCoord, TGeomap, TTypePlaceObj, TWhatTodoObj } from "@/interface";
import {
    arrow_up,
    place_url,
    type_place_list_url,
    what_todo_url,
} from "@/pages/MapApp.vue";
import VButton from "@/stylecomponents/VButton.vue";
import { mapState } from "vuex";

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
    computed: {
        ...mapState("geomap", [
            "select_channel_geomap",
            "coordinat_click",
            "RefMapContainer",
        ]),
    },
    methods: {
        hidden_elm() {
            this.$emit("hidden_elm");
        },
        async create_geomap() {
            console.log("Отправка: создание нового места");
            const coord: TCoord = this.coordinat_click;
            console.log(this.$refs);
            const req = {
                cord_x: coord.latitude,
                cord_y: coord.longitude,
                simpl_name: this.shortName,
                rating: this.rating,
                address: "",
                channel_geomap: this.select_channel_geomap.id,
                what_todo: this.todo.map((element) => element.id),
                type_place: this.typePlace.id,
            };
            const res = await PostJsonFromUrl(place_url, req);
            if (res.ok) {
                alert("Успешное создание нового места");
                this.hidden_elm();
                this.$emit("hiddenOverBox");
                // Если произошло успешное создание,
                // 1. Добавляем маркер на карту
                this.RefMapContainer._setMarkersFromGeomap(
                    <TGeomap>JSON.parse(res.data)
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
