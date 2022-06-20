<template>
	<div class="locations">
		<Map class="locations-map" :zoom="4" :geojson-cluster="posts_geojson" />
	</div>
</template>

<script>
import { mapState } from 'pinia';
import { usePosts } from '@/stores/posts';
import Map from '@/components/Map';

import flow from 'lodash/fp/flow';
import filter from 'lodash/fp/filter';
import groupBy from 'lodash/fp/groupBy';
import pickBy from 'lodash/fp/pickBy';
import map from 'lodash/fp/map';
import sortBy from 'lodash/fp/sortBy';
import reverse from 'lodash/fp/reverse';
import meanBy from 'lodash/meanBy';

export default {
	// layout: 'no-container',
	components: {
		Map,
	},

	setup() {
		const store = usePosts();
		store.load();
	},

	computed: {
		...mapState(usePosts, ['postsList', 'locations', 'mentions']),

		mood_locations() {
			return flow(
				filter('location_verbose'),
				filter('mood'),
				groupBy('location_verbose'),
				pickBy((entries, _) => entries.length >= 5),
				map((entries, location) => [location, meanBy(entries, (entry) => entry.mood).toPrecision(3)]),
				sortBy(1),
				reverse,
			)(this.postsList);
		},
/*
		posts_geojson() {
			const geojson = {
				name: 'markers',
				type: 'FeatureCollection',
				features: [],
			};

			for (const post of this.posts) {
				if (!post.location_lon || !post.location_lat) {
					continue;
				}

				geojson.features.push({
					type: 'Feature',
					properties: { label: `<a href="/posts/${post.id}">${post.date}</a>` },
					geometry: {
						type: 'Point',
						coordinates: [post.location_lon, post.location_lat],
					},
				});
			}

			return geojson;
		},
*/

	},
};
</script>

<style lang="scss">
.locations {
	// FIXME - Hacky. Should just use a different layout
	position: fixed;
	margin-top: 53px;
	top: 0;
	left: 0;
	height: calc(100% - 53px);
	width: 100%;

	.locations-map {
		height: 100%;
		width: 100%;
	}
}
</style>
