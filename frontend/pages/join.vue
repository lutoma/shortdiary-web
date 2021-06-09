<template>
	<div class="login">
		<h1>Join shortdiary</h1>

		<el-form ref="signup_form" :model="user" :rules="rules" label-width="100px">
			<el-form-item v-if="get_error('non_field_errors')">
				<el-alert :title="get_error('non_field_errors')" :closable="false" type="error" />
			</el-form-item>

			<el-form-item label="Username" prop="username" :error="get_error('username')">
				<el-input ref="username" placeholder="Username" v-model="user.username" @keyup.enter.native="signup" required autofocus />
			</el-form-item>

			<el-form-item label="Email" prop="email" :error="get_error('email')">
				<el-input placeholder="Email" v-model="user.email" @keyup.enter.native="signup" required autofocus />
			</el-form-item>

			<el-form-item label="Password" prop="password" :error="get_error('password')">
				<el-input placeholder="Password" v-model="user.password" @keyup.enter.native="signup" show-password required />
			</el-form-item>

			<el-form-item :error="get_error('captcha')">
				<!--<vue-hcaptcha ref="captcha" :reCaptchaCompat="false" size="invisible" sitekey="9cdd09c8-ab67-4728-b301-8e957d5ef4d8" /> -->
				<vue-hcaptcha
					ref="captcha"
					:reCaptchaCompat="false"
					size="invisible"
					sitekey="9cdd09c8-ab67-4728-b301-8e957d5ef4d8"
					@verify="captcha_verified" />
			</el-form-item>

			<el-form-item>
				<el-button type="primary" @click="signup" :loading.sync="loading"><fa :icon="['far', 'sign-in']" /> Sign in</el-button>
			</el-form-item>
		</el-form>

		<p class="hcaptcha-info">This site is protected by hCaptcha and its <a href="https://hcaptcha.com/privacy" rel="nofollow noopener" target="_blank">Privacy Policy</a> and <a href="https://hcaptcha.com/terms" rel="nofollow noopener" target="_blank">Terms of Service</a> apply.</p>
	</div>
</template>

<script>
import VueHcaptcha from '@hcaptcha/vue-hcaptcha'
import { get_error } from '~/assets/utils'

export default {
	auth: 'guest',

	components: {
		VueHcaptcha
	},

	mounted() {
		this.$refs.username.$el.children[0].focus()
	},

	data() {
		return {
			loading: false,
			error: {},
			user: {
				username: '',
				email: '',
				password: '',
				captcha: ''
			},
			rules: {
				username: [{ required: true, message: 'Please enter a username', trigger: 'change' }],
				email: [{ required: true, type: 'email', message: 'Please enter a valid email address', trigger: 'change' }],
				password: [{ required: true, message: 'Please enter a password', trigger: 'change' }]
			}
		}
	},

	methods: {
		get_error,

		async captcha_verified(token, ekey) {
			this.user.captcha = token
			this.loading = true

			try {
				// Reset auth - This is needed to make sure we don't
				// send an (outdated) Authorization header during the
				// signup request
				this.$auth.reset({ resetInterceptor: false })
				await this.$axios.$post('/user/signup/', this.user)
				const res = await this.$axios.$post('/auth/login/', this.user)
				this.$auth.setUserToken(res.access, res.refresh)
			} catch (err) {
				this.error = err.response.data
			} finally {
				this.loading = false
			}
		},

		signup() {
			this.error = null

			this.$refs.signup_form.validate(valid => {
				if (valid) {
					this.$refs.captcha.execute()
				}
			})
		}
	},

	head () {
		return { title: 'Join – shortdiary' }
	}
}
</script>

<style lang="scss">
.login {
	.el-form {
		max-width: 600px;
	}

	.hcaptcha-info {
		font-size: 12px;
		color: #909399;
		margin-top: 4rem;
	}
}
</style>
