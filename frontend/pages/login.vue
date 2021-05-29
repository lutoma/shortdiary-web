<template>
	<div class="login">
		<template v-if="!mfa_request.method">
			<h1>Sign in</h1>

			<el-form ref="login_form" :model="credentials" :rules="rules" label-width="100px" v-if="!mfa_request.method">
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
		</template>

		<template v-if="mfa_request.method">
			<h1>Two-factor authentication</h1>

			<p v-if="mfa_request.method == 'app'">Please enter the code from your token generator.</p>
			<el-form ref="mfa_form" :model="mfa_request" :rules="mfa_rules" label-width="100px">
				<el-form-item>
					<el-alert v-if="error" :title="error" :closable="false" type="error" />
				</el-form-item>
				<el-form-item label="Code" prop="code">
					<el-input ref="code" placeholder="Code" v-model="mfa_request.code" @keyup.enter.native="mfaConfirm" required autofocus />
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="mfaConfirm" :loading.sync="loading"><fa :icon="['far', 'sign-in']" /> Confirm sign-in</el-button>
				</el-form-item>
			</el-form>
		</template>

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
			},

			mfa_rules: {
				code: [{ required: true, message: 'Please enter the authentication code', trigger: 'change' }]
			},
			mfa_request: {
				code: '',
				ephemeral_token: '',
				method: ''
			}
		}
	},

	methods: {
		login() {
			this.error = null

			this.$refs.login_form.validate(async valid => {
				if (valid) {
					this.loading = true

					try {
						// Reset auth - This is needed to make sure we don't
						// send an (outdated) Authorization header during the
						// login request
						this.$auth.reset({ resetInterceptor: false })

						const res = await this.$axios.$post('/auth/login/', this.credentials)

						if ('ephemeral_token' in res) {
							this.mfa_request = res
							this.$refs.code.$el.children[0].focus()
						} else {
							this.$auth.setUserToken(res.access, res.refresh)
						}
					} catch (err) {
						this.error = err.response.data.non_field_errors[0]
					} finally {
						this.loading = false
					}
				}
			})
		},

		mfaConfirm() {
			this.error = null

			this.$refs.mfa_form.validate(async valid => {
				if (valid) {
					this.loading = true

					try {
						const res = await this.$axios.$post('/auth/login/code/', this.mfa_request)
						this.$auth.setUserToken(res.access, res.refresh)
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
