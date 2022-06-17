<template>
	<div class="login">
		<h1>See you soon</h1>
		<div v-loading="this.loading">You have been logged out successfully</div>
	</div>
</template>

<script>
export default {
	async mounted() {
		await this.$auth.logout()
		this.loading = false
		this.$router.go('/')
	},

	data() {
		return {
			loading: true,
		}
	},
}
</script>
