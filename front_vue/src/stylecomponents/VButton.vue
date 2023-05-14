<template>
    <button class="custom-button" @click="handleClick">{{ value }}</button>
</template>

<script>
export default {
    props: {
        value: {
            type: [String, Number],
            required: true
        }
    },
    methods: {
        handleClick() {
            this.$emit('clickBt', this.value);
        }
    }
};
</script>

<style lang="scss" scoped>
@import "@/gcolor.scss";

.custom-button {
    display: inline-block;
    padding: 1rem 1rem;
    font-size: 1.3rem;

    font-weight: bold;
    text-align: center;
    color: #ffffff;
    background-color: $ЦветФона;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    box-shadow: 0px 0px 0.1rem 0.1rem $ЦветФонаВсплывающегоОкна;

    width: 100%;

    &:hover {
        background-color: #45a049;

    }

    &:focus {
        outline: none;
        box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
    }

}
</style>
