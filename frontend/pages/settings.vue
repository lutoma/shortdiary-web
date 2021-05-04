<template>
	<div class="settings">
		<h1>Settings</h1>

		<el-row :gutter="50">
			<el-col :span="12">
				<el-card>
					<h2>Account</h2>
					<el-form ref="form" :model="user" label-position="left" label-width="200px">
						<el-form-item label="Username">
							<el-input v-model="user.username" />
						</el-form-item>
						<el-form-item label="Email">
							<el-input v-model="user.email" />
						</el-form-item>
						<p><n-link to="/change-password">Change password</n-link></p>
					</el-form>
				</el-card>
			</el-col>

			<el-col :span="12">
				<el-card>
					<h2>Privacy</h2>
					<el-form ref="form" :model="user" label-position="left" label-width="200px">
						<el-form-item label="Add location to posts">
							<el-switch v-model="user.geolocation_enabled" />
						</el-form-item>

						<el-form-item label="Include me in leaderboard">
							<el-switch v-model="user.include_in_leaderboard" />
						</el-form-item>
					</el-form>
				</el-card>
			</el-col>
		</el-row>

		<el-button type="primary" @click="saveSettings">Save settings</el-button>
	</div>
</template>

<script>
export default {
	data() {
		return {
			user: JSON.parse(JSON.stringify(this.$auth.user))
		}
	},

	methods: {
		async saveSettings() {
			// FIXME error handling
			await this.$axios.$patch('/user/', this.user)
			await this.$auth.fetchUser()
			this.$message({ type: 'success', message: 'Your settings have been saved.' })
		}
	},

	head () {
		return { title: 'Settings – shortdiary' }
	}
}
</script>

<style>
.settings .el-card {
	margin-bottom: 30px;
}
</style>
