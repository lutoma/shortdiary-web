<template>
	<div class="dashboard">
		<el-backtop />
		<PostTimeline />
	</div>
</template>

<script>
import PostTimeline from '~/components/PostTimeline'

export default {
	components: {
		PostTimeline
	}
}
</script>

<style lang="scss">
.dashboard {
	height: 100%;
}
</style>
