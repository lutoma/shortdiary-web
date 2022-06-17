<template>
	<div class="edit-post" v-loading="!this.post">
		<h1>Edit entry</h1>
		<PostEditor :post="post" v-if="post" />
	</div>
</template>

<script>
import PostEditor from '~/components/PostEditor'

export default {
	components: {
		PostEditor
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
		return { title: 'Edit entry – shortdiary' }
	}
}
</script>

<style lang="scss">
.edit-post {
	height: 100%;
	display: flex;
	flex-direction: column;
	padding-bottom: 30px;

	.post-editor {
		width: 100%;
		flex-grow: 1;
	}
}
</style>
