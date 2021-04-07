<template>
	<div class="login">
		<h1>Join shortdiary</h1>

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
				<vue-hcaptcha sitekey="9cdd09c8-ab67-4728-b301-8e957d5ef4d8" />
			</el-form-item>

			<el-form-item>
				<el-button type="primary" @click="join" :loading.sync="loading"><fa :icon="['far', 'sign-in']" /> Sign in</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
import VueHcaptcha from '@hcaptcha/vue-hcaptcha'

export default {
	auth: 'guest',

	components: {
		VueHcaptcha
	},

	mounted() {
		//this.$refs.username.$el.children[0].focus()
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
		join() {
		}
	}

}
</script>

<style lang="scss">
.login .el-form {
	max-width: 600px;
}
</style>
