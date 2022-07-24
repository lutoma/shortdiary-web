<template>
	<div class="settings">
		<h1>Settings</h1>

		<el-tabs v-model="$route.name" class="settings-tabs" tab-position="top" @tab-click="changeTab">
			<el-tab-pane v-for="tab in tabs" :key="tab.route" :name="tab.route" :label="tab.name" />
		</el-tabs>

		<RouterView />
	</div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const tabs = [
	{ name: 'Account', route: 'account-settings' },
	{ name: 'Billing', route: 'billing-settings' },
	{ name: 'Data export', route: 'data-export' },
];

const router = useRouter();
const changeTab = async (obj, _ev) => {
	router.push({ name: obj.paneName });
};
</script>

<style lang="scss">
.settings {
	.settings-tabs {
		.el-tabs__content {
			padding-top: 1rem;
		}
	}
}
</style>
