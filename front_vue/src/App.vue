<template>
    <router-view></router-view>
</template>

<script lang="ts">

export default {
    // // Компоненты
    // components: {},
    // // Аргументы
    // //props: {},
    // // Переменные
    // data() {
    //     return {
    //         // ИмяПеременной: ЗначениеПоУмолчанию,
    //     };
    // },
    // // Методы
    // methods: {},
};
</script>
<style lang="scss">
@import "@/gcolor.scss";

html,
body {
    height: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
    background: $ЦветФонаВсплывающегоОкна;
}
#app {
    width: 100%;
    height: 100%;
}
</style>
