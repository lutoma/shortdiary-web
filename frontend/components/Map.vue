<template>
	<div id="map-wrapper">&nbsp;</div>
</template>

<script>
import 'mapbox-gl/dist/mapbox-gl.css'
import mapboxgl from 'mapbox-gl/dist/mapbox-gl.js'

export default {
	props: {
		center: { type: Array, default: () => [8.4320361, 49.5001306] },
		zoom: { type: Number, default: 12 },
		markers: { type: Array, default: () => [] },
		controls: { type: Boolean, default: true }
	},

	mounted() {
		mapboxgl.accessToken = 'pk.eyJ1IjoibHV0b21hIiwiYSI6ImVkbzF4MG8ifQ.pIpC2pu9savl1ZZLl8TGrA'
		mapboxgl.baseApiUrl = 'https://shortdiary.com/map'

		const map = new mapboxgl.Map({
			container: 'map-wrapper',
			style: 'mapbox://styles/lutoma/cko3qggqm0cce17o6itr6j044?optimize=true',
			center: this.center,
			zoom: this.zoom,
			scrollZoom: false

		})

		if (this.controls) {
			const nav = new mapboxgl.NavigationControl()
			map.addControl(nav, 'top-right')
		}

		for (const marker of this.markers) {
			new mapboxgl.Marker({ color: '#CDB380' })
				.setLngLat(marker)
				.addTo(map)
		}
	}
}
</script>
