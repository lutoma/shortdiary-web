export const state = () => ({
	posts: null
})

export const actions = {
	async updatePosts({ commit }) {
		if (this.state.posts !== null) {
			return
		}

		const { data } = await this.$axios.get('/posts/')
		commit('SET_POSTS', data)
	}
}

export const mutations = {
	SET_POSTS(state, data) {
		state.posts = data
	}
}
