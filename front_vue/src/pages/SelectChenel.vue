<template>
    <div class="container">
        <h1>Список каналов</h1>
        <div class="box_extra" v-show="select_elm == undefined">
            <VButton
                class="row"
                v-for="channel in channels"
                :key="channel.id"
                :value="channel.name"
                @click="selectChannel(channel)" />
        </div>
    </div>
</template>

<script lang="ts">
import { channel_geomap } from "@/pages/MapApp.vue";
import { DownloadFromUrl, TFromUrl } from "@/helper";
import { UrlGetParams, TChannelGeomapObj } from "@/interface";
import VButton from "@/stylecomponents/VButton.vue";
import { mapActions } from "vuex";

export default {
    components: { VButton },
    data() {
        return {
            channels: <TChannelGeomapObj[]>[],
        };
    },
    async mounted() {
        await this.fetchChannels();
    },
    methods: {
        ...mapActions("geomap", ["Update_select_channel"]),
        async fetchChannels() {
            const channels: TFromUrl = await DownloadFromUrl(channel_geomap);
            if (channels.ok) {
                this.channels = channels.data;
            } else {
                console.error("Не удалось получить список каналов");
            }
        },

        selectChannel(channel: TChannelGeomapObj) {
            this.Update_select_channel({
                channel: channel,
                router: this.$router,
                route: this.$route,
            });
            const c = UrlGetParams.channel;
            this.$router.push({ name: "main_map", query: { c: channel.id } });
            return;
        },
    },
};
</script>

<style scoped lang="scss">
@import "@/gcolor.scss";

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background: $ЦветФона;
    width: 100%;
    height: 100%;
}

h1 {
    margin-bottom: 1rem;
    background: transparent;
    color: $БазовыйЦветТекста;
}

.box_extra {
    display: flex;
    flex-direction: column;
    height: auto;
    overflow: auto;
    width: 50%;

    .row {
        box-shadow: 0px 0px 4rem 0.7rem $ЦветФонаВсплывающегоОкна;
        border-radius: 0.5rem;
        margin-top: 0.1rem;
        background: transparent;
        outline: none;
        font-size: 1rem;
        margin-bottom: 0.3rem;
        text-align: left;

        &:hover {
            background: $ЦветФонаВсплывающегоОкна;
        }
    }
}
</style>
