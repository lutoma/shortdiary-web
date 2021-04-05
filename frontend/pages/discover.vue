<template>
	<div>
		<h1>Discover</h1>
		<Post :post="post" v-if="post" v-loading="!post" />
	</div>
</template>

<script>
import Post from '~/components/Post'

export default {
	components: {
		Post
	},

	data() {
		return {
			post: null
		}
	},

	async fetch() {
		this.post = await this.$axios.$get('/posts/random_public/')
	},
}
</script>

<style lang="scss">
.post-timeline {
	.post {
		margin: 30px 0;
	}
}
</style>
