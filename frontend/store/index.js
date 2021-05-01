export const state = () => ({
	posts: [],
	posts_update: null
})

export const mutations = {
	setPosts(state, data) {
		state.posts = data
		state.posts_update = new Date()
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
	}
}
