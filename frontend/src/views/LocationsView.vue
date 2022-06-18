<template>
	<div class="locations">
		<Map class="locations-map" :zoom="4" :geojson-cluster="posts_geojson" />
	</div>
</template>

<script>
import { mapState } from 'pinia';
import { usePosts } from '@/stores/posts';
import PostLengthChart from '@/components/PostLengthChart.js';
import EqualHeightRow from '@/components/EqualHeightRow.vue';
import PaginatedTableCard from '@/components/PaginatedTableCard.vue';
import Map from '@/components/Map';
import _ from 'lodash';

export default {
	// layout: 'no-container',
	components: {
		PostLengthChart,
		EqualHeightRow,
		PaginatedTableCard,
		Map,
	},

	setup() {
		const store = usePosts();
		store.load();
	},

	data() {
		return {
			top_locations_page: 1,
			top_mentions_page: 1,
			top_mood_locations_page: 1,
			time_frame: 'all',
		};
	},

	computed: {
		...mapState(usePosts, ['posts', 'top_locations', 'top_mentions']),

		top_mood_locations() {
			return _(this.posts)
				.filter('location_verbose')
				.filter('mood')
				.groupBy('location_verbose')
				.pickBy((entries, _) => entries.length >= 5)
				.map((entries, location) => [location, _.meanBy(entries, (entry) => entry.mood).toPrecision(3)])
				.sortBy(1)
				.reverse()
				.value();
		},

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

	},

	head() {
		return { title: 'Stats – shortdiary' };
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
