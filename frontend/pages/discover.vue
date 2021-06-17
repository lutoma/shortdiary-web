<template>
	<div class="discover">
		<h1>Discover public posts</h1>

		<el-backtop />
		<vue-masonry-wall :items="posts" :options="{width: 600, padding: 16}" :ssr="{columns: 2}" @append="loadMore">
			<template v-slot:default="{item}">
				<Post :post="item" :compact="true" />
			</template>
		</vue-masonry-wall>

		<div class="more">
			<h2>Hold up, loading more posts …</h2>
		</div>
	</div>
</template>

<script>
import Post from '~/components/Post'
import VueMasonryWall from 'vue-masonry-wall'

export default {
	components: {
		Post,
		VueMasonryWall
	},

	data() {
		return {
			posts: []
		}
	},

	async fetch() {
		this.posts = await this.$axios.$get('/posts/random_public/')
	},

	methods: {
		loadMore() {
			this.$axios.$get('/posts/random_public/').then(posts => {
				this.posts.push(...posts)
			})
		}
	},

	head () {
		return { title: 'Discover – shortdiary' }
	}
}
</script>

<style>
.discover .more {
	margin-top: 5rem;
	text-align: center;
}
</style>
