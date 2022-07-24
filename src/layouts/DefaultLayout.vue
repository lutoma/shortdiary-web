<template>
	<div id="default-layout-container">
		<Navigation />
		<div id="main-container">
			<div class="main-alerts">
				<el-alert
					v-if="!auth.haveSubscription"
					class="subscription-alert"
					type="warning"
				>
					Your subscription has expired. You can still view and delete your entries, but edits and new entries require a subscription.<br><br>
					<router-link :to="{ name: 'billing-settings' }">
						<el-button type="primary" size="small">
							Update subscription
						</el-button>
					</router-link>
				</el-alert>

				<el-alert
					v-if="store.legacyPosts.length"
					class="subscription-alert"
					type="warning"
				>
					Shortdiary now supports client-side encryption. Your account still has {{ store.legacyPosts.length }} unencrypted older posts.<br><br>
					<router-link :to="{ name: 'posts-migrate' }">
						<el-button type="primary" size="small">
							Encrypt existing posts
						</el-button>
					</router-link>
				</el-alert>
			</div>

			<RouterView />
		</div>
	</div>
</template>

<script setup>
import Navigation from '@/components/Navigation.vue';
import { usePosts } from '@/stores/posts';
import { useAuth } from '@/stores/auth';

const auth = useAuth();
auth.loadUser();

const store = usePosts();
store.load();
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

		.main-alerts {
			margin-bottom: 1rem;

			.el-alert {
				margin-bottom: 1rem;
			}
		}
	}
}
</style>
