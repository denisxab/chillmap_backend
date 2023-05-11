<!-- Это компонент для создание нового места в БД -->
<template>
    <div class="box_extra">
        <label class="row">
            <div class="label">* Короткое имя:</div>
            <input v-model="shortName" />
        </label>
        <label class="row">
            <div class="label">* Рейтинг места:</div>
            <input v-model="rating" type="number" min="0" max="5" />
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
        <input
            class="send_bt"
            type="button"
            value="Отправить"
            @click="create_geomap" />
        <input
            ref="hidden_elm"
            class="hidden_elm"
            type="image"
            @click="hidden_elm" />
    </div>
</template>

<script lang="ts">
import { DownloadFromUrl, PostJsonFromUrl } from "@/helper";
import { TCoord, TTypePlaceObj, TWhatTodoObj } from "@/interface";
import {
    arrow_up,
    place_url,
    type_place_list_url,
    what_todo_url,
} from "@/pages/MapApp.vue";

export default {
    emits: ["hidden_elm", "hiddenOverBox"],
    mounted() {
        this.$refs["hidden_elm"].src = arrow_up;
        this.show();
    },
    data() {
        return {
            shortName: "",
            rating: 0,
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

            const req = {
                cord_x: coord.latitude,
                cord_y: coord.longitude,
                simpl_name: this.shortName,
                rating: this.rating,
                address: "",
                channel_geomap: this.$store.state.geomap.select_channel_geomap,
                what_todo: this.todo.map((element) => element.id),
                type_place: this.typePlace.id,
            };
            const res = await PostJsonFromUrl(place_url, req);
            if (res.ok) {
                alert("Успешное создание нового места");
                this.hidden_elm();
                this.$emit("hiddenOverBox");
            } else {
                alert("Ошибка создания нового места");
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
    }
}
</style>
