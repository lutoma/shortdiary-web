<template>
	<div id="map-background">
		<Map class="map" :controls="false" :center="center" :zoom="11" />
	</div>
</template>

<script>
import Map from '~/components/Map'

export default {
	components: {
		Map
	},

	props: {
		center: { type: Array, default: () => [8.4320361, 49.5001306] }
	}
}
</script>

<style lang="scss">
#map-background {
	position: fixed;
	top: 0;
	left: 0;
	height: 100%;
	width: 100%;

	z-index: -1;
	pointer-events: none;

	.map {
		height: 100%;
		width: 100%;
	}
}
</style>
