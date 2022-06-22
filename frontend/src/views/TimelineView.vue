<template>
	<div class="timeline">
		<el-dialog v-model="editorOpen" custom-class="post-editor-dialog" width="80%" top="70px" :destroy-on-close="true" :before-close="handleEditorClose">
			<template #header>
				<h2>{{ editorTitle }}</h2>
			</template>
			<RouterView />
		</el-dialog>
		<el-backtop />
		<PostTimeline />
	</div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessageBox } from 'element-plus';
import PostTimeline from '@/components/PostTimeline.vue';

const route = useRoute();
const router = useRouter();

const editorOpen = ref(route.name !== 'timeline');
const editorTitle = computed(() => {
	if (route.name === 'edit-post') {
		return 'Edit entry';
	}

	return 'Create a new entry';
});

watch(route, (to) => {
	editorOpen.value = (to.name !== 'timeline');
});

const handleEditorClose = (done) => {
	ElMessageBox.confirm('Are you sure you want to discard your changes?')
		.then(() => {
			router.push({ name: 'timeline' });
			done();
		})
};
</script>

<style lang="scss">
.timeline {
	height: 100%;

	.post-editor-dialog {
		.el-dialog__header {
			h2 {
				margin: 0;
			}
		}

		.el-dialog__body {
			padding-top: .5rem;
		}
	}
}
</style>
