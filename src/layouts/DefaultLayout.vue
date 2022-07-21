<template>
	<div id="default-layout-container">
		<Navigation />
		<div id="main-container">
			<el-alert
				v-if="!auth.haveSubscription"
				class="subscription-alert"
				type="warning"
				title="Your subscription/trial has expired. You will still be able to view and delete your entries, but new entries or edits require a subscription."
			/>

			<RouterView />
		</div>
	</div>
</template>

<script setup>
import Navigation from '@/components/Navigation.vue';
import { useAuth } from '@/stores/auth';

const auth = useAuth();
auth.loadUser();
</script>

<style lang='scss'>
@use "@/assets/main.scss" as *;

#default-layout-container {
	// Fixed menu
	padding-left: 240px;

	#main-container {
		flex-grow: 1;
		height: 100vh;
		margin-top: 30px;
		padding: 0 2rem;

		display: flex;
		flex-direction: column;
	}

	.subscription-alert {
		margin-bottom: 2rem;
	}
}
</style>
