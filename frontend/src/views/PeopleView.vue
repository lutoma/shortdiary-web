<template>
	<div class="people">
		<h1>People</h1>
	</div>
</template>

<script setup>
import { usePosts } from '@/stores/posts';

const store = usePosts();
store.load();
</script>

<style lang="scss">
.people {

}
</style>
