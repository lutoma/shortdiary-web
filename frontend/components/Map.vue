<template>
	<div id="map-wrap">
		<client-only>
			<l-map :zoom="this.zoom" :center="this.center" :options="Object.assign({attributionControl: false}, this.options)">
				<l-tile-layer url="/map/tiles/{z}/{x}/{y}.png" />
				<l-control-attribution position="topright" prefix='<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>' />
				<l-marker v-if="this.markers" v-for="marker of this.markers" :key="marker" :lat-lng="marker" />
			</l-map>
		</client-only>
	</div>
</template>


<script>
export default {
	props: {
		center: { type: Array, default: () => [49.5001306, 8.4320361] },
		zoom: { type: Number, default: 12 },
		markers: { type: Array, default: () => [] },
		options: { type: Object, default: () => {} },
	},
}
</script>
