import _ from 'lodash'

export const state = () => ({
	posts: [],
	posts_update: null,
	top_mentions: []
})

export const mutations = {
	setPosts(state, data) {
		state.posts = data
		state.posts_update = new Date()
	},

	setTopMentions(state, data) {
		state.top_mentions = data
	}
}

export const actions = {
	async updatePosts({ commit }) {
		const update_delta = new Date() - this.state.posts_update
		if (this.state.post_update !== null && update_delta < 15000) {
			return
		}

		const { data } = await this.$axios.get('/posts/')
		commit('setPosts', data)

		// Extract top mentions for use in stats.vue and PostEditor component
		const mentions = []
		for (const post of data) {
			// FIXME Should deduplicate/DRYfy regex with Post.vue
			// Temporarily cast to Set to deduplicate mentions within a post
			mentions.push(...[...new Set(post.text.toLowerCase().match(/@\w+\b/g))])
		}

		const top_mentions = _(mentions)
			.countBy()
			.toPairs()
			.sortBy(1)
			.reverse()
			.value()

		commit('setTopMentions', top_mentions)
	}
}
