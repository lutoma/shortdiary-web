<template>
	<div class="login">
		<template v-if="!mfaRequest.method">
			<h1>Sign in</h1>

			<el-form v-if="!mfaRequest.method" ref="loginFormElement" :model="credentials" :rules="rules" label-width="100px">
				<el-form-item>
					<el-alert v-if="error" :title="error" :closable="false" type="error" />
				</el-form-item>

				<el-form-item label="Username" prop="username">
					<el-input ref="nameElement" v-model="credentials.username" placeholder="Username" required autofocus @keyup.enter="login" />
				</el-form-item>
				<el-form-item label="Password" prop="password">
					<el-input v-model="credentials.password" placeholder="Password" show-password required @keyup.enter="login" />
				</el-form-item>
				<el-form-item>
					<el-button v-model:loading="loading" type="primary" @click="login">
						<fa :icon="['far', 'sign-in']" /> Sign in
					</el-button>
				</el-form-item>
			</el-form>
		</template>

		<template v-if="mfaRequest.method">
			<h1>Two-factor authentication</h1>

			<p v-if="mfaRequest.method == 'app'">
				Please enter the code from your token generator.
			</p>
			<el-form ref="mfa_form" :model="mfaRequest" :rules="mfaRules" label-width="100px">
				<el-form-item>
					<el-alert v-if="error" :title="error" :closable="false" type="error" />
				</el-form-item>
				<el-form-item label="Code" prop="code">
					<el-input ref="code" v-model="mfaRequest.code" placeholder="Code" required autofocus @keyup.enter="mfaConfirm" />
				</el-form-item>
				<el-form-item>
					<el-button v-model:loading="loading" type="primary" @click="mfaConfirm">
						<fa :icon="['far', 'sign-in']" /> Confirm sign-in
					</el-button>
				</el-form-item>
			</el-form>
		</template>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useAuth } from '@/stores/auth';
import { useRouter } from 'vue-router';

const store = useAuth();
const router = useRouter();

const nameElement = ref(null);
onMounted(() => {
	nameElement.value.$el.children[0].children[0].focus();
});

const loading = ref(false);
const error = ref(null);
const credentials = reactive({
	username: '',
	password: '',
});

const rules = {
	username: [{ required: true, message: 'Please enter a username', trigger: 'change' }],
	password: [{ required: true, message: 'Please enter a password', trigger: 'change' }],
};

const mfaRules = {
	code: [{ required: true, message: 'Please enter the authentication code', trigger: 'change' }],
};

const mfaRequest = reactive({
	code: '',
	ephemeral_token: '',
	method: '',
});

const loginFormElement = ref(null);
function login() {
	error.value = null;

	loginFormElement.value.validate(async (valid) => {
		if (valid) {
			loading.value = true;

			try {
				await store.login(credentials.username, credentials.password);
				router.push({ name: 'dashboard' });
			} catch (err) {
				error.value = err.toString();
			} finally {
				loading.value = false;
			}
		}
	});
}

function mfaConfirm() {
	error.value = null;
/*
	$refs.mfa_form.validate(async (valid) => {
		if (valid) {
			loading.value = true;

			try {
				const res = await $axios.$post('/auth/login/code/', mfaRequest);
				$auth.setUserToken(res.access, res.refresh);
				$router.push({ name: 'dashboard' });
			} catch (err) {
				error.value = err.response.data.non_field_errors[0];
			} finally {
				loading.value = false;
			}
		}
	});
*/
}
</script>

<style lang="scss">
.login .el-form {
	max-width: 600px;
}
</style>
