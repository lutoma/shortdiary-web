<template>
	<div class="post-detail">
		<Post :post="post" v-if="post" v-loading="!post" />
		<div id="map-background" v-if="post && post.location_lon && post.location_lat">
			<Map class="map" :center="[post.location_lon, post.location_lat]" :zoom="11" :controls="false" />
		</div>
	</div>
</template>

<script>
import Post from '~/components/Post'
import Map from '~/components/Map'

export default {
	auth: 'guest',
	components: {
		Post,
		Map
	},

	data() {
		return {
			post: null
		}
	},

	async fetch() {
		this.post = await this.$axios.$get(`/posts/${this.$route.params.pathMatch}/`)
	},

	head () {
		if (!this.post) {
			return {}
		}

		const date = new Date(this.post.date)
		const title = `Entry on ${date.toLocaleString('en', { month: 'long' })} ${date.getDate()}, ${date.getFullYear()} – shortdiary`
		const desc = this.post.text.length > 250 ? `${this.post.text.substring(0, 250)}…` : this.post.text

		const meta = [
			{ hid: 'og:title', property: 'og:title', content: title },
			{ hid: 'twitter:title', name: 'twitter:title', content: title },
			{ hid: 'description', name: 'description', content: desc },
			{ hid: 'og:description', property: 'og:description', content: desc },
			{ hid: 'twitter:description', name: 'twitter:description', content: desc }
		]

		if (this.post.image) {
			meta.push(
				{ hid: 'og:image', property: 'og:image', content: this.post.image },
				{ hid: 'twitter:image', name: 'twitter:image', content: this.post.image }
			)
		}

		return { title, meta }
	}
}
</script>

<style lang="scss">
.post-detail {
	#map-background {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		width: 100%;

		z-index: -1;
		pointer-events: none;

		.map {
			height: 100%;
			width: 100%;
		}
	}
}
</style>
