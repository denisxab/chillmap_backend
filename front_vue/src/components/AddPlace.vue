<template>
    <div>

        <button @click="hidden_elm"></button>
    </div>
</template>

<script lang="ts">
export default {
    emits: ["hidden_elm"],
    methods: {
        hidden_elm() {
            this.$emit("hidden_elm");
        }
    }
}
</script>

<style lang="scss" scoped>
@import "@/gcolor.scss";
</style>