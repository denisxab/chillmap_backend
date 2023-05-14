<template>
    <div class="channel-list">
        <h1>Список каналов</h1>
        <div v-for="channel in channels" :key="channel.id">
            <button class="channel-button" @click="selectChannel(channel)">{{ channel.name }}</button>
        </div>
    </div>
</template>

<script lang="ts" >
import { channel_geomap } from "@/pages/MapApp.vue";
import { DownloadFromUrl, TFromUrl } from "@/helper";
import { UrlGetParams, TChannelGeomapObj } from "@/interface";

export default {
    data() {
        return {
            channels: <TChannelGeomapObj[]>[]
        };
    },
    async mounted() {
        await this.fetchChannels();
    },
    methods: {
        async fetchChannels() {
            const channels: TFromUrl = await DownloadFromUrl(
                channel_geomap
            );
            if (channels.ok) {
                this.channels = channels.data;
            }
            else {
                console.error('Не удалось получить список каналов')
            }
        },

        selectChannel(channel: TChannelGeomapObj) {
            this.$store.dispatch('geomap/Update_select_channel', {
                channel: channel,
                router: this.$router,
                route: this.$route,
            });
            const c = UrlGetParams.channel
            this.$router.push({ name: 'main_map', query: { c: channel.id } });
            return
        }
    },
};
</script>

<style scoped lang="scss">
@import "@/gcolor.scss";

h1 {
    color: $h_color;
    background: transparent;
    text-align: center;
}

.channel-list {
    max-width: 400px;
    margin: 0 auto;
}

.channel-button {
    display: block;
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    background-color: #f0f0f0;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.channel-button:hover {
    background-color: #e0e0e0;
}

.channel-button:focus {
    outline: none;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
}
</style>
