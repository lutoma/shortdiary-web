<template>
	<div class="join">
		<h2>Join shortdiary</h2>

		<el-form ref="signupFormElement" :model="user" :rules="rules" label-position="top">
			<el-form-item v-if="error">
				<el-alert :title="error" :closable="false" type="error" />
			</el-form-item>

			<el-form-item label="Email" prop="email">
				<el-input ref="emailElement" v-model="user.email" placeholder="Email" required size="large" @keyup.enter="signup" autofocus />
			</el-form-item>

			<el-form-item label="Password" prop="password">
				<el-input v-model="user.password" placeholder="Password" show-password required size="large" @keyup.enter="signup" />
			</el-form-item>

			<el-form-item>
				<el-button v-model:loading="loading" size="large" type="primary" @click="signup">
					<fa :icon="['far', 'sign-in']" /> Sign up
				</el-button>
			</el-form-item>
		</el-form>

		<p class="signup-prompt">
			Already have an account? <router-link :to="{ name: 'login' }">Sign in</router-link>
		</p>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/stores/auth';

const emailElement = ref(null);
onMounted(() => {
	emailElement.value.$el.children[0].children[0].focus();
});

const auth = useAuth();
const router = useRouter();

const loading = ref(false);
const error = ref(null);
const user = reactive({
	email: '',
	password: '',
});

const rules = {
	password: [{ required: true, message: 'Please enter a password', trigger: 'blur' }],
	email: [{
		required: true, type: 'email', message: 'Please enter a valid email address', trigger: 'blur',
	}],
};

const signupFormElement = ref(null);
function signup() {
	error.value = null;

	signupFormElement.value.validate(async (valid) => {
		if (valid) {
			loading.value = true;

			try {
				await auth.signup(user);
				await auth.login(user.email, user.password);
				router.push({ name: 'dashboard' });
			} catch (err) {
				error.value = err.toString();
			} finally {
				loading.value = false;
			}
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
}
</style>
