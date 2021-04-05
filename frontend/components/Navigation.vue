<template>
	<div class="main-nav-container">
		<nav>
			<div class="name"><n-link :to="$auth.loggedIn ? '/dashboard' : '/'">shortdiary</n-link></div>
			<el-menu :default-active="$route.path" mode="horizontal" class="main-nav" @select="navSelect">
				<el-menu-item v-for="item of nav_items" :key="item.path" :index="item.path">{{ item.label }}</el-menu-item>
			</el-menu>
			<el-menu mode="horizontal" @select="navSelect" v-if="$auth.loggedIn">
				<el-menu-item index="/settings"><fa :icon="['fas', 'wrench']" /></el-menu-item>
				<el-menu-item index="logout"><fa :icon="['fas', 'sign-out']" /></el-menu-item>
			</el-menu>
		</nav>
	</div>
</template>

<script>
export default {
	methods: {
		navSelect(path, _) {
			// Bit hacky
			if(path === 'logout') {
				this.$auth.logout()
				this.$router.push('/', () => {
					this.$message({ type: 'success', message: 'You have been logged out.' });
				})
			} else {
				this.$router.push({path})
			}
		},

	},
	data() {
		let nav_items;
		if(this.$auth.loggedIn) {
			nav_items = [
				{path: '/dashboard', label: 'Dashboard'},
				{path: '/new', label: 'New entry'},
				{path: '/discover', label: 'Discover'},
				{path: '/stats', label: 'Stats'},
				{path: '/leaderboard', label: 'Leaderboard'},
			]
		} else {
			nav_items = [
				{path: '/login', label: 'Sign in'},
				{path: '/signup', label: 'Join'},
			]
		}

		return { nav_items }
	}
}
</script>

<style lang="scss">
.main-nav-container {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	z-index: 2000;

	background: #036564;
	border-bottom: 3px solid #CDB380;
	box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

	.main-nav {
		flex-grow: 1;
	}

	nav {
		max-width: 1600px;
		padding: 0 2rem;

		margin: 0 auto;
		display: flex;
		align-items: center;

		.name {
			font-size: 25px;
			font-weight: 600;
			margin-right: 50px;

			&, a {
				color: white;
				text-decoration: none;
			}
		}

		.el-menu--horizontal {
			border-bottom: none;
			background: initial;

			.el-menu-item, .el-submenu .el-submenu__title {
				color: white;
				font-weight: 600;
				border-right: solid #025554 1px;
				height: 50px;
				line-height: 50px;
				font-size: .9rem;

				&:first-of-type {
					border-left: solid #025554 1px;
				}
			}

			.el-menu-item.is-active, .el-menu-item:not(.is-disabled):focus, .el-menu-item:not(.is-disabled):hover {
				border-bottom: none;
				background-color: rgba(0, 0, 0, 0.1);
				color: white;
			}
		}
	}
}
</style>
