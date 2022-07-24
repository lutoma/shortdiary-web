<template>
	<el-form ref="form" :model="user" label-position="left" label-width="200px">
		<el-form-item label="Email">
			<el-input v-model="user.email" @keyup.enter="saveSettings" />
		</el-form-item>
		<el-form-item label="Password">
			<router-link to="/change-password">
				Change password
			</router-link>
		</el-form-item>

		<el-form-item>
			<el-button type="primary" @click="saveSettings">
				Save changes
			</el-button>
		</el-form-item>
	</el-form>
</template>

<script setup>
import { reactive } from 'vue';
import { useAuth } from '@/stores/auth';
import pick from 'lodash/pick';

const auth = useAuth();
auth.loadUser();
const user = reactive(pick(auth.user, ['email']));

function saveSettings() {
	auth.updateUser(user);
}
</script>
