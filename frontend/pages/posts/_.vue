<template>
	<div>
		<h1>Post</h1>
		<Post :post="post" v-if="post" v-loading="!post" :show-permalink="false" />
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
		this.post = await this.$axios.$get(`/posts/${ this.$route.params.pathMatch }/`)
	},
}
</script>
