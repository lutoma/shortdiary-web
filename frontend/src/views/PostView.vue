<template>
	<div class="post-detail">
		<Post :post="post" v-if="post" v-loading="!post" />
		<MapBackground v-if="post && post.location_lon && post.location_lat" :center="[post.location_lon, post.location_lat]" />
	</div>
</template>

<script>
import Post from '@/components/Post.vue';
import MapBackground from '@/components/MapBackground.vue';

export default {
	auth: false,
	components: {
		Post,
		MapBackground,
	},

	data() {
		return {
			post: null,
		};
	},

	async fetch() {
		this.post = await this.$axios.$get(`/posts/${this.$route.params.pathMatch}/`);
	},
};
</script>
