<template>
	<div class="edit-post">
		<h1>Edit entry</h1>
		<PostEditor :post="post" v-if="post" />
	</div>
</template>

<script setup>
import PostEditor from '@/components/PostEditor.vue'
import { usePosts } from '@/stores/posts';
import { useRoute } from 'vue-router'

const route = useRoute();
const store = usePosts();
const id = route.params.id;
let post = null;

// FIXME super inefficient
for (const npost of store.posts) {
	if (npost.id == id) {
		post = npost;
	}
}
</script>

<style lang="scss">
.edit-post {
	height: 100%;
	display: flex;
	flex-direction: column;
	padding-bottom: 30px;

	.post-editor {
		width: 100%;
		flex-grow: 1;
	}
}
</style>
