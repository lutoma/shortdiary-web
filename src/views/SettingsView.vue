<template>
	<div class="settings">
		<h1>Settings</h1>

		<el-tabs class="settings-tabs" tab-position="left">
			<el-tab-pane label="Account">
				<el-form ref="form" :model="user" label-position="left" label-width="200px">
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
			</el-tab-pane>

			<el-tab-pane label="Billing">
				<p v-if="auth.haveSubscription">
					You are currently on the {{ auth.user.subscription.plan_name }} plan.
				</p>
				<p v-else>
					You do not currently have an active plan.
				</p>

				<el-button v-if="auth.haveSubscription" type="primary" @click="handlePortal">
					Manage your subscription
				</el-button>

				<el-button v-else type="primary" @click="handleSubscribe">
					Choose a plan
				</el-button>
			</el-tab-pane>
		</el-tabs>
	</div>
</template>

<script setup>
import { reactive, computed } from 'vue';
import { useAuth } from '@/stores/auth';
import api from '@/api';
import pick from 'lodash/pick';

const auth = useAuth();
auth.loadUser();
const user = reactive(pick(auth.user, ['email']));

function saveSettings() {
	auth.updateUser(user);
}

const handleSubscribe = (async () => {
	const res = await api.post('/billing/subscribe');
	window.location.href = res.data.session_url;
});

const handlePortal = (async () => {
	const res = await api.post('/billing/portal');
	window.location.href = res.data.session_url;
});

</script>

<style lang="scss">
.settings {
	.settings-tabs {
		height: 500px;

		.el-tabs__content {
			padding: 1rem 0.6rem;
			padding-top: 0;
			padding-left: 3rem;
		}
	}
}
</style>
