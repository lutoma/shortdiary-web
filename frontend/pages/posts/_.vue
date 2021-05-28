<template>
	<div class="post-detail">
		<Post :post="post" v-if="post" v-loading="!post" />
		<MapBackground v-if="post && post.location_lon && post.location_lat" :center="[post.location_lon, post.location_lat]" />
	</div>
</template>

<script>
import Post from '~/components/Post'
import MapBackground from '~/components/MapBackground'

export default {
	auth: false,
	components: {
		Post,
		MapBackground
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
