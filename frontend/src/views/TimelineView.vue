<template>
	<div class="timeline">
		<el-card v-if="editor_visible" id="new-post-overlay">
			<PostEditor />
		</el-card>

		<el-backtop />
		<PostTimeline />
	</div>
</template>

<script setup>
import PostTimeline from '@/components/PostTimeline.vue';
import PostEditor from '@/components/PostEditor.vue';
</script>

<style lang="scss">
.timeline {
	height: 100%;

	#new-post-overlay {
		position: fixed;
		top: 150px;
		left: 100px;
		height: calc(100% - 250px);
		width: calc(100% - 200px);
		z-index: 100;

		display: flex;
		flex-direction: column;

		> .el-card__body {
			display: flex;
			flex-grow: 1;
			flex-direction: column;
		}
	}
}
</style>
