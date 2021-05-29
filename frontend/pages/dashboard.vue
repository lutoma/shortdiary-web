<template>
	<div class="dashboard">
		<PostTimeline />
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
</style>
