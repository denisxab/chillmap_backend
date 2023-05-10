<!-- Компонент для отображения поверхностной информации о маркере  -->
<template>
    <div class="map_facile">
        <!--Тип места  -->
        <div class="cel name_marker">
            <div class="img">
                <img ref="img_name_marker" />
            </div>
            <div class="text">
                {{ name_marker }}
            </div>
        </div>
        <!-- Имя места -->
        <div class="cel simpl_name">
            <div class="img">
                <img ref="img_simpl_name" />
            </div>
            <div class="text">
                {{ simpl_name }}
            </div>
        </div>
        <!-- Рейтинга -->
        <div class="cel rating">
            <div class="img">
                <img ref="img_rating" />
            </div>
            <div class="text">
                {{ rating }}
            </div>
        </div>
        <!-- Адреса -->
        <div class="cel address">
            <div class="img">
                <img ref="img_address" />
            </div>
            <div class="text">
                {{ address }}
            </div>
        </div>
        <!-- Чем тут можно заняться -->
        <div class="cel">
            <ParamsList v-if="whattodo && whattodo.length > 0" :params_list="whattodo" />
        </div>
    </div>
</template>
<script lang="ts">
import { ParseUrlSrc, getAddress, whattodoIdFromName } from "@/helper";
import ParamsList from "@/components/ParamsList.vue";
import { TPropertiesMark } from "@/interface";

const name_marker = ParseUrlSrc("@/img/name_marker.svg");
const simpl_name = ParseUrlSrc("@/img/simpl_name.svg");
const rating = ParseUrlSrc("@/img/rating.svg");
const address = ParseUrlSrc("@/img/address.svg");

export default {
    components: { ParamsList },
    data() {
        return {
            name_marker: undefined,
            simpl_name: undefined,
            rating: undefined,
            address: undefined,
            whattodo: undefined,
        };
    },
    mounted() {
        this.$refs["img_name_marker"].src = name_marker;
        this.$refs["img_simpl_name"].src = simpl_name;
        this.$refs["img_rating"].src = rating;
        this.$refs["img_address"].src = address;
    },
    methods: {

    },
    watch: {
        props_component: {
            async handler(newValue: TPropertiesMark) {
                // Эти данные берутся из поверхностной информации
                this.name_marker = newValue.type_place_obj.name;
                this.simpl_name = newValue.simpl_name;
                this.rating = newValue.rating;
                this.address = newValue.address;
                this.whattodo = whattodoIdFromName(newValue);
                this.address = await getAddress(newValue.cord_x, newValue.cord_y)
            },
            deep: true,
        },
    },
    computed: {
        // Отслеживание изменений выбранного маркера
        props_component() {
            return this.$store.state.geomap.select_PropertiesMark;
        },
    },
};
</script>
<style lang="scss" scoped>
@import "@/gcolor.scss";

.map_facile {
    color: $ПриглушенныйЦветТекста;
    margin: 0.6rem;

    .cel {
        display: flex;

        .img {
            margin-right: 10px;

            img {
                width: 1rem;
                height: 1rem;
            }
        }
    }
}
</style>
