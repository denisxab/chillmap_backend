<template>
    <div class="container">
        <div class="box_extra" v-show="select_elm == undefined">
            <div class="row" @click="handleClick('add_place')">
                Создать новое место в выбранной точки
            </div>
            <div class="row" @click="handleClick('login')">Вход</div>
            <div class="row" @click="handleClick('registration')">
                Регистрация
            </div>
            <div class="row" @click="handleClick('about')">О проекте</div>
        </div>
        <div class="box_select_elm">
            <AddPlace
                ref="add_place"
                v-show="select_elm === 'add_place'"
                @hidden_elm="hidden_elm" />
        </div>
    </div>
</template>

<script lang="ts">
import AddPlace from "@/components/AddPlace.vue";

export default {
    components: {
        AddPlace,
    },
    data() {
        return {
            select_elm: <string>undefined,
        };
    },
    methods: {
        // Обработчик нажатия на строку
        async handleClick(link: string) {
            await this.$refs[link].show();
            this.select_elm = link;
        },
        hidden_elm() {
            this.select_elm = undefined;
        },
    },
};
</script>

<style lang="scss" scoped>
@import "@/gcolor.scss";

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 5rem;
}

.box_extra {
    display: flex;
    flex-direction: column;
    height: auto;

    .row {
        box-shadow: 0px 0px 4rem 0.7rem $ЦветФонаВсплывающегоОкна;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        padding: 1.3rem;
        overflow: hidden;
        font-size: 1.5rem;
        text-align: center;

        &:hover {
            background: $ЦветФонаВсплывающегоОкна;
        }
    }
}
</style>
