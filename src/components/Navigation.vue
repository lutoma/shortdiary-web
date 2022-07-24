<template>
	<el-menu
		id="main-nav"
		:default-active="$route.name"
		background-color="#036564"
		text-color="#ffffff"
		class="primary-menu"
		@select="navSelect"
	>
		<el-menu-item index="dashboard">
			<fa :icon="['far', 'house']" /> Home
		</el-menu-item>

		<el-menu-item index="timeline">
			<fa :icon="['far', 'list']" /> Entries
		</el-menu-item>

		<el-menu-item index="people">
			<fa :icon="['far', 'users']" /> People
		</el-menu-item>

		<el-menu-item index="locations">
			<fa :icon="['far', 'map-marked-alt']" /> Places
		</el-menu-item>

		<el-menu-item index="trackables">
			<fa :icon="['far', 'chart-mixed']" /> Trackables
		</el-menu-item>

		<div style="flex-grow: 1;" />

		<el-menu-item index="logout">
			<fa :icon="['far', 'sign-out']" /> <span>Sign out</span>
		</el-menu-item>
		<el-menu-item index="account-settings">
			<fa :icon="['far', 'gear']" /> <span>Settings</span>
		</el-menu-item>

		<div class="nav-footer">
			<a href="https://github.com/lutoma/shortdiary-web" target="_blank" rel="noopener">Source code</a>
			<a href="https://fnordserver.eu/en/imprint/" target="_blank" rel="noopener">Legal notice</a>
			<a href="https://fnordserver.eu/en/privacy-policy/" target="_blank" rel="noopener">Privacy</a>
		</div>
	</el-menu>
</template>

<script setup>
import { useAuth } from '@/stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuth();
const router = useRouter();

const navSelect = (name, _) => {
	if (name === 'logout') {
		auth.logout();
		router.push({ name: 'login' });
	} else {
		router.push({ name });
	}
};
</script>

<style lang="scss">
	#main-nav {
		position: fixed;
		height: 100vh;
		width: 240px;
		z-index: 100;
		top: 0;
		left: 0;
		display: flex;
		flex-direction: column;
		background-color: #036564;
		user-select: none;

		.primary-menu {
			flex-grow: 1;
			margin-top: 2rem;
		}

		.nav-avatar {
			width: 25px;
			height: 25px;
			border-radius: 50%;
			margin-right: 15px;
		}

		a {
			color: #ffffff !important;
		}

		.nav-footer {
			font-size: .75rem;
			color: #dedede;

		}
	}
</style>
