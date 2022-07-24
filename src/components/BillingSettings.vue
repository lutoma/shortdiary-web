<template>
	<p v-if="auth.haveSubscription" style="margin-top: 0;">
		You are currently on the {{ auth.user.subscription.plan_name }} plan.
	</p>
	<p v-else style="margin-top: 0;">
		You do not currently have an active plan.
	</p>

	<el-button v-if="auth.haveSubscription && auth.user.subscription.plan != 'earlyadopter'" type="primary" :loading="loadingStripeURL" @click="handlePortal">
		Manage your subscription
	</el-button>

	<el-button v-else type="primary" :loading="loadingStripeURL" @click="handleSubscribe">
		Choose a plan
	</el-button>
</template>

<script setup>
import { ref } from 'vue';
import { useAuth } from '@/stores/auth';
import api from '@/api';

const auth = useAuth();
auth.loadUser();
const loadingStripeURL = ref(false);

const handleSubscribe = (async () => {
	loadingStripeURL.value = true;
	const res = await api.post('/billing/subscribe');
	loadingStripeURL.value = false;
	window.location.href = res.data.session_url;
});

const handlePortal = (async () => {
	loadingStripeURL.value = true;
	const res = await api.post('/billing/portal');
	loadingStripeURL.value = false;
	window.location.href = res.data.session_url;
});

</script>
