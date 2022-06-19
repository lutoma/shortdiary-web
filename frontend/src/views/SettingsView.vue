<template>
	<div class="settings">
		<h1>Settings</h1>

		<el-row :gutter="30">
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
						<el-form-item label="Password">
							<n-link to="/change-password">
								Change password
							</n-link>
						</el-form-item>
					</el-form>
				</el-card>

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
									<!--<el-button size="small" v-if="!scope.row.is_primary" @click="mfaSwitchPrimary(scope.row.name)">Make primary</el-button>-->
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

		<el-button type="primary" @click="saveSettings">
			Save settings
		</el-button>
	</div>
</template>

<script>
import MfaSetup from '@/components/MfaSetup.vue';

export default {
	components: {
		MfaSetup,
	},
	data() {
		return {
			user: 'dummyuser',
			mfa_config: {
				methods: [],
			},

			mfa_methods: null,
			mfa_setup_visible: false,
		};
	},

	async fetch() {
		this.mfa_config = await this.$axios.$get('/auth/mfa/config/');
		await this.loadMfaMethods();
	},

	computed: {
		mfa_can_add() {
			return this.mfa_methods.length < this.mfa_config.methods.length;
		},
	},

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
		*/

		mfaSetupDone() {
			this.loadMfaMethods();
			this.mfa_setup_visible = false;
			this.$message({ type: 'success', message: 'Authentication method has been added' });
		},
	},
};
</script>

<style>
.settings .el-card {
	margin-bottom: 30px;
}
</style>
