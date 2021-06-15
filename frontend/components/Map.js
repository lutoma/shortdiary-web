import 'mapbox-gl/dist/mapbox-gl.css'
import mapboxgl from 'mapbox-gl/dist/mapbox-gl.js'

let map = null

function add_cluster(map, geojson) {
	map.addSource('posts', {
		type: 'geojson',
		data: geojson,
		cluster: true,
		clusterMaxZoom: 14,
		clusterRadius: 50
	})

	map.addLayer({
		id: 'clusters',
		type: 'circle',
		source: 'posts',
		filter: ['has', 'point_count'],
		paint: {
			'circle-color': '#CDB380',
			'circle-radius': [
				'step',
				['get', 'point_count'],
				15,
				30, 17,
				50, 20,
				80, 22,
				100, 25
			]
		}
	})

	map.addLayer({
		id: 'cluster-count',
		type: 'symbol',
		source: 'posts',
		filter: ['has', 'point_count'],
		layout: {
			'text-field': '{point_count_abbreviated}',
			'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
			'text-size': 12
		}
	})

	map.addLayer({
		id: 'unclustered-point',
		type: 'circle',
		source: 'posts',
		filter: ['!', ['has', 'point_count']],
		paint: {
			'circle-color': '#CDB380',
			'circle-radius': 6,
			'circle-stroke-width': 1,
			'circle-stroke-color': '#fff'
		}
	})

	// inspect a cluster on click
	map.on('click', 'clusters', e => {
		const features = map.queryRenderedFeatures(e.point, {
			layers: ['clusters']
		})

		const clusterId = features[0].properties.cluster_id

		map.getSource('posts').getClusterExpansionZoom(
			clusterId, (err, zoom) => {
				if (err) {
					return
				}

				map.easeTo({
					center: features[0].geometry.coordinates,
					zoom: zoom
				})
			}
		)
	})

	map.on('click', 'unclustered-point', function (e) {
		const coordinates = e.features[0].geometry.coordinates.slice()
		const label = e.features[0].properties.label

		if (!label) {
			return
		}

		// Ensure that if the map is zoomed out such that
		// multiple copies of the feature are visible, the
		// popup appears over the copy being pointed to.
		while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
			coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
		}

		new mapboxgl.Popup()
			.setLngLat(coordinates)
			.setHTML(label)
			.addTo(map)
	})

	// This seems stupidly hacky but it's 1:1 from the Mapbox documentation so idk
	map.on('mouseenter', 'clusters', () => {
		map.getCanvas().style.cursor = 'pointer'
	})

	map.on('mouseleave', 'clusters', () => {
		map.getCanvas().style.cursor = ''
	})

	map.on('mouseenter', 'unclustered-point', () => {
		map.getCanvas().style.cursor = 'pointer'
	})

	map.on('mouseleave', 'unclustered-point', () => {
		map.getCanvas().style.cursor = ''
	})
}

export default {
	props: {
		center: { type: Array, default: () => [8.4320361, 49.5001306] },
		zoom: { type: Number, default: 12 },
		markers: { type: Array, default: () => [] },
		controls: { type: Boolean, default: true },
		geojsonCluster: { type: Object, default: () => {} }
	},

	render(createElement) {
		return createElement('div', { attrs: { id: 'map-wrapper' } })
	},

	mounted() {
		mapboxgl.accessToken = 'pk.eyJ1IjoibHV0b21hIiwiYSI6ImVkbzF4MG8ifQ.pIpC2pu9savl1ZZLl8TGrA'
		mapboxgl.baseApiUrl = 'https://beta.shortdiary.com/map'

		map = new mapboxgl.Map({
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

		map.on('load', () => {
			if (this.markers.length > 1) {
				const bounds = new mapboxgl.LngLatBounds()

				for (const marker of this.markers) {
					bounds.extend(marker)
				}

				console.log('bounds are', bounds)
				map.fitBounds(bounds)
			}

			for (const marker of this.markers) {
				new mapboxgl.Marker({ color: '#CDB380' })
					.setLngLat(marker)
					.addTo(map)
			}

			if (this.geojsonCluster) {
				add_cluster(map, this.geojsonCluster)
			}
		})
	},

	watch: {
		center() {
			map.jumpTo({ center: this.center })
		}
	}
}
