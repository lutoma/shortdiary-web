<template>
	<div class="login">
		<h1>Sign in</h1>

		<el-form ref="form" :model="credentials" :rules="rules" label-width="100px">
			<el-form-item>
				<el-alert v-if="error" :title="error" :closable="false" type="error" />
			</el-form-item>

			<el-form-item label="Username" prop="username">
				<el-input ref="username" placeholder="Username" v-model="credentials.username" @keyup.enter.native="login" required autofocus />
			</el-form-item>
			<el-form-item label="Password" prop="password">
				<el-input placeholder="Password" v-model="credentials.password" @keyup.enter.native="login" show-password required />
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="login" :loading.sync="loading"><fa :icon="['far', 'sign-in']" /> Sign in</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
export default {
	auth: 'guest',

	mounted() {
		this.$refs.username.$el.children[0].focus()
	},

	data() {
		return {
			loading: false,
			error: null,
			credentials: {
				username: '',
				password: ''
			},
			rules: {
				username: [{ required: true, message: 'Please enter a username', trigger: 'change' }],
				password: [{ required: true, message: 'Please enter a password', trigger: 'change' }]
			}
		}
	},

	methods: {
		login() {
			this.error = null
			this.loading = true

			this.$refs.form.validate(async valid => {
				if (valid) {
					try {
						await this.$auth.loginWith('local', { data: this.credentials })
						this.$router.go('/dashboard')
					} catch (err) {
						this.error = err.response.data.non_field_errors[0]
					} finally {
						this.loading = false
					}
				}
			})
		}
	},

	head () {
		return { title: 'Login – shortdiary' }
	}

}
</script>

<style lang="scss">
.login .el-form {
	max-width: 600px;
}
</style>
