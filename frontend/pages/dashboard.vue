<template>
	<div class="dashboard">
		<PostTimeline>
			<template v-slot:sidebar>
				<div class="dashboard-sidebar-header" v-loading="!$auth.user">
					<GravatarImg :email="$auth.user.email" :size="65" class="avatar" />
					<h2>Hi {{ $auth.user.username }}!</h2>
					<p>Here's how you're doing:</p>

					<ul class="stats">
						<li>{{ $auth.user.streak }} day streak</li>
						<li>{{ $auth.user.posts_count }} total posts</li>
						<li>{{ $auth.user.post_chars }} total chars</li>
					</ul>
				</div>
			</template>
		</PostTimeline>
	</div>
</template>

<script>
import PostTimeline from '~/components/PostTimeline'
import GravatarImg from '~/components/GravatarImg'

export default {
	components: {
		PostTimeline,
		GravatarImg
	}
}
</script>

<style lang="scss">
.dashboard {
	height: 100%;
}

.dashboard-sidebar-header {
	margin-bottom: 2rem;

	.avatar {
		float: right;
		width: 65px;
		height: 65px;
		border-radius: 50%;
	}
}
</style>
