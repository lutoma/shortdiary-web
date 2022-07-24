<template>
	<p style="margin-top: 0;">
		You can export your posts as machine-readable JSON files
	</p>

	<el-button type="primary" @click="doExport">
		Download posts as ZIP file
	</el-button>
</template>

<script setup>
import { ref } from 'vue';
import { useAuth } from '@/stores/auth';
import { usePosts } from '@/stores/posts';
import JSZip from 'jszip';
import saveAs from 'jszip/vendor/FileSaver';
import api from '@/api';

const auth = useAuth();
const store = usePosts();
auth.loadUser();
store.load();

const doExport = (async () => {
	console.log('data-export');
	const zip = new JSZip();
	const postsDir = zip.folder('posts');

	for (const [_, post] of store.posts) {
		postsDir.file(`${post.date}.json`, JSON.stringify(post));
	}

	zip.generateAsync({ type: 'blob' })
		.then((content) => {
			saveAs(content, 'shortdiary-export.zip');
		});
});
</script>
