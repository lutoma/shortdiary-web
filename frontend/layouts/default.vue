<template>
	<div id="default-layout-container">
		<Navigation />
		<div id="main-container">
			<nuxt/>
		</div>
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
