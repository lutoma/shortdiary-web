<template>
	<div id="default-layout-container">
		<Navigation />
		<div id="main-container">
			<RouterView />
		</div>
	</div>
</template>

<script setup>
import Navigation from '@/components/Navigation.vue';
</script>

<style lang='scss'>
@use "@/assets/main.scss" as *;

#default-layout-container {
	// Fixed top menu
	padding-top: 50px;

	#main-container {
		flex-grow: 1;
		width: 100%;
		max-width: 1600px;
		min-width: 1200px;
		margin: 0 auto;
		margin-top: 30px;
		padding: 0 1rem;
	}
}
</style>
