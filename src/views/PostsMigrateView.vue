<template>
	<div class="posts-migrate">
		<h1>Update your posts</h1>

		<template v-if="!store.legacyPosts.length">
			<p>All your posts already use the current format version.</p>
		</template>

		<template v-else>
			<el-button v-if="!running" type="primary" @click="migrate">
				Start encrypting your post
			</el-button>

			<div v-if="running" class="migration-progress">
				<el-progress :percentage="progressPercentage" :pstatus="progressStatus" />
			</div>
		</template>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { usePosts } from '@/stores/posts';

const running = ref(false);
const progressPercentage = ref(0);
const progressStatus = ref('');

const store = usePosts();
store.load(true);

const migrate = async () => {
	running.value = true;

	let converted = 0;
	store.legacyPosts.forEach(async (id) => {
		const post = store.posts.get(id);
		console.log(id, post);

		await store.store_post(post, false);
		converted += 1;
		progressPercentage.value = Math.round((converted / store.legacyPosts.length) * 100);
	});

	progressStatus.value = 'success';
};
</script>
