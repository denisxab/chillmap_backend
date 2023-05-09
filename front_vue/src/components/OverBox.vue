<!-- Окно поверх остальных -->
<template>
    <div class="over_box_comp" @keyup.esc="hiddenOverBox" tabindex="0">
        <!-- Список компонентов на всплывающем окне -->
        <div class="over_box_body">
            <!-- Детальная информация о месте -->
            <DetailFromPlace v-show="view_component == 'DetailFromPlace'" />
        </div>
        <!-- Пустой div чтобы можно было больше проскролить вниз -->
        <div class="empty"></div>
        <!-- Кнопка для скрытия всплывающего окна -->
        <input ref="hidden_over_box" class="hidden_over_box" type="image" @click="hiddenOverBox" />
    </div>
</template>
<script lang="ts">
import { arrow_up } from "@/pages/MapApp.vue";
import DetailFromPlace from "@/components/DetailFromPlace.vue";

export default {
    emits: ["hidden_over_box"],
    components: { DetailFromPlace },
    props: {
        view_component: { type: Object as () => string },
    },
    mounted() {
        this.$refs["hidden_over_box"].src = arrow_up;
    },
    // Методы
    methods: {
        // Скрыть всплывающие окно
        hiddenOverBox() {
            this.$emit("hidden_over_box");
        },
    },
};
</script>
<style lang="scss" scoped>
@import "@/gcolor.scss";

.over_box_comp {
    position: absolute;
    z-index: 99;
    background: $ЦветФона;
    color: $БазовыйЦветТекста;
    width: 100%;
    min-height: 100%;

    .over_box_body {}

    .hidden_over_box {
        position: fixed;
        border: none;
        bottom: 10px;
        right: 10px;
        width: 4rem;
        height: 4rem;
        -webkit-transform: rotate(90deg);
        -moz-transform: rotate(90deg);
        -o-transform: rotate(90deg);
        -ms-transform: rotate(90deg);
        transform: rotate(90deg);
    }

    .empty {
        height: 10rem;
    }
}
</style>
