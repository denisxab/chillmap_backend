<!-- Отображает список объектов в виде плиток -->
<template>
    <div class="params_list">
        <div class="li_h" v-for="(item, index) in params_list" :key="index">
            <a
                target="_blank"
                :href="item"
                v-if="typeof item == 'string' && item.includes('://')"
                >{{ item }}</a
            >
            <span v-else>
                {{ item }}
            </span>
        </div>
    </div>
</template>
<script lang="ts">
export default {
    // Аргументы
    props: {
        params_list: {
            type: Object as () => string[] | number[],
        },
    },
};
</script>
<style lang="scss" scoped>
@import "@/gcolor.scss";

.params_list {
    margin-top: 0.3rem;
    display: flex;
    flex-wrap: wrap;
    .li_h {
        background: $ЦветФонаПодсказки;
        color: $ЯркоеВыделение;
        margin-left: 0.2rem;
        margin-bottom: 0.3rem;
        box-shadow: inset 0px 0px 4px 1px #000;
        padding: 0.3rem;
        border-radius: 0.5rem;
    }
    a {
        //  Убрать подчёркивание ссылки
        text-decoration: none;
        color: $ЯркоеВыделение;
    }
}
</style>
