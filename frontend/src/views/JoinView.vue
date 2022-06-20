<template>
	<div class="join">
		<h2>Join shortdiary</h2>

		<el-form ref="signupFormElement" :model="user" :rules="rules" label-position="top">
			<el-form-item v-if="error">
				<el-alert :title="error" :closable="false" type="error" />
			</el-form-item>

			<el-form-item label="Username" prop="name">
				<el-input ref="nameElement" v-model="user.name" placeholder="Username" required size="large" autofocus @keyup.enter="signup" />
			</el-form-item>

			<el-form-item label="Email" prop="email">
				<el-input v-model="user.email" placeholder="Email" required size="large" @keyup.enter="signup" />
			</el-form-item>

			<el-form-item label="Password" prop="password">
				<el-input v-model="user.password" placeholder="Password" show-password required size="large" @keyup.enter="signup" />
			</el-form-item>

			<el-form-item>
				<!--<vue-hcaptcha ref="captcha" :reCaptchaCompat="false" size="invisible" sitekey="9cdd09c8-ab67-4728-b301-8e957d5ef4d8" /> -->
				<!--<vue-hcaptcha
					ref="captcha"
					:reCaptchaCompat="false"
					size="invisible"
					sitekey="9cdd09c8-ab67-4728-b301-8e957d5ef4d8"
					@verify="captcha_verified" />-->
			</el-form-item>

			<el-form-item>
				<el-button v-model:loading="loading" size="large" type="primary" @click="signup">
					<fa :icon="['far', 'sign-in']" /> Sign up
				</el-button>
			</el-form-item>
		</el-form>

		<p class="signup-prompt">Already have an account? <router-link :to="{ name: 'login' }">Sign in</router-link></p>

		<p class="hcaptcha-info">
			This site is protected by hCaptcha and its <a href="https://hcaptcha.com/privacy" rel="nofollow noopener" target="_blank">Privacy Policy</a> and <a href="https://hcaptcha.com/terms" rel="nofollow noopener" target="_blank">Terms of Service</a> apply.
		</p>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useAuth } from '@/stores/auth';
import VueHcaptcha from '@hcaptcha/vue-hcaptcha';

const nameElement = ref(null);
onMounted(() => {
	nameElement.value.$el.children[0].children[0].focus();
});

const loading = ref(false);
const error = ref(null);
const user = reactive({
	name: '',
	email: '',
	password: '',
	captcha: '',
});

const rules = {
	name: [{ required: true, message: 'Please enter a username', trigger: 'change' }],
	password: [{ required: true, message: 'Please enter a password', trigger: 'change' }],
	email: [{
		required: true, type: 'email', message: 'Please enter a valid email address', trigger: 'change',
	}],
};

async function captchaVerified(token, _ekey) {
	user.captcha = token;
	loading.value = true;
	const auth = useAuth();

	await auth.signup(user);
	loading.value = false;

	/*
	try {
		await auth_store.signup(user);
	} catch (err) {
		error.value = err.response.data
	} finally {
		loading.value = false
	}
	*/
}

const signupFormElement = ref(null);
function signup() {
	error.value = null;

	signupFormElement.value.validate((valid) => {
		if (valid) {
			captchaVerified();
			// this.$refs.captcha.execute()
		}
	});
}
</script>

<style lang="scss">
.join {
	.el-button {
		width: 100%;
	}

	.login-prompt {
		margin-top: 2rem;
	}

	.hcaptcha-info {
		font-size: 12px;
		color: #909399;
		margin-top: 4rem;
		margin-bottom: 0;
	}
}
</style>
