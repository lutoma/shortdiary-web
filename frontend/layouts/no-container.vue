<template>
	<div id="default-layout-container">
		<Navigation />
		<nuxt/>
	</div>
</template>

<script>
import Navigation from '~/components/Navigation'

export default {
	components: {
		Navigation
	}
}
</script>

<style lang='scss'>
@import "~assets/main.scss";
</style>
