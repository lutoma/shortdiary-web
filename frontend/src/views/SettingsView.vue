<template>
	<div class="settings">
		<h1>Settings</h1>

		<el-row :gutter="30">
			<el-col :span="12">
				<el-card>
					<el-form ref="form" :model="user" label-position="left" label-width="200px">
						<h2>Account</h2>
						<el-form-item label="Email">
							<el-input v-model="user.email" @keyup.enter="saveSettings" />
						</el-form-item>
						<el-form-item label="Password">
							<n-link to="/change-password">
								Change password
							</n-link>
						</el-form-item>

						<el-form-item>
							<el-button type="primary" @click="saveSettings">
								Save changes
							</el-button>
						</el-form-item>
					</el-form>
				</el-card>

<!--
				<el-dialog v-model:visible="mfa_setup_visible" title="Two-factor authentication setup" width="550px">
					<MfaSetup :config="mfa_config" :active_methods="mfa_methods" @success="mfaSetupDone" />
				</el-dialog>

				<el-card v-loading="mfa_methods === null">
					<h2>Two-factor authentication</h2>
					<template v-if="mfa_methods && !mfa_methods.length">
						<el-button size="medium" @click="mfa_setup_visible = true">
							Enable two-factor authentication
						</el-button>
					</template>
					<template v-if="mfa_methods && mfa_methods.length">
						<el-table :data="mfa_methods" :show-header="false" style="width: 100%">
							<el-table-column prop="name" label="Method">
								<template #default="scope">
									{{ mfaMethodName(scope.row.name) }} <template v-if="scope.row.is_primary">
										(Primary)
									</template>
								</template>
							</el-table-column>
							<el-table-column label="Actions" align="right">
								<template #default="scope">
									<!- -<el-button size="small" v-if="!scope.row.is_primary" @click="mfaSwitchPrimary(scope.row.name)">Make primary</el-button>- ->
									<el-button size="small" type="danger" @click="mfaDelete(scope.row.name)">
										Delete
									</el-button>
								</template>
							</el-table-column>
						</el-table>
						<el-button v-if="mfa_can_add" size="medium" style="margin-top: 1rem" @click="mfa_setup_visible = true">
							Add authentication method
						</el-button>
					</template>
				</el-card>
-->
			</el-col>
		</el-row>
	</div>
</template>

<script setup>
import { reactive } from 'vue';
import { useAuth } from '@/stores/auth';
import pick from 'lodash/pick';
//import MfaSetup from '@/components/MfaSetup.vue';

const auth = useAuth();
const user = reactive(pick(auth.user, ['email']));

function saveSettings() {
	auth.updateUser(user);
}

/*
methods: {
	async loadMfaMethods() {
		this.mfa_methods = await this.$axios.$get('/auth/mfa/user-active-methods/');
	},

	async saveSettings() {
		// FIXME error handling
		await this.$axios.$patch('/user/', this.user);
		await this.$auth.fetchUser();
		this.$message({ type: 'success', message: 'Your settings have been saved.' });
	},

	mfaMethodName(name) {
		const names = Object.fromEntries(this.mfa_config.methods);
		if (!(name in names)) {
			return '?';
		}

		return names[name];
	},

	async mfaDelete(name) {
		await this.$axios.$post(`/auth/${name}/deactivate/`);
		this.loadMfaMethods();
	},

	/*
	mfaSwitchPrimary(name) {
		this.$axios.$post('/auth/code/request/').then(() => {
			this.$prompt('Please enter a verification code').then(({ value }) => {
				this.$axios.$post('/auth/mfa/change-primary-method/', { method: name, code: value })
				this.$message({ type: 'success', message: 'Your primary two-factor authentication method has been changed.' })
				this.loadMfaMethods()
			})
		})
	},

	mfaSetupDone() {
		this.loadMfaMethods();
		this.mfa_setup_visible = false;
		this.$message({ type: 'success', message: 'Authentication method has been added' });
	},
	*/
</script>

<style>
.settings .el-card {
	margin-bottom: 30px;
}
</style>
