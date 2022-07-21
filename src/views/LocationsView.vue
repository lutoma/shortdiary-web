<template>
	<div class="locations">
		<h1>Places</h1>

		<Map class="locations-map" :zoom="4" :geojson-cluster="postsGeojson" />

		<EqualHeightRow>
			<el-col :span="12">
				<PaginatedTable title="Frequent locations" icon="map-marked-alt" :data="store.locations">
					<el-table-column prop="0" label="Location">
						<template #default="scope">
							<router-link :to="{ name: 'timeline', query: { location: scope.row[0] } }">
								{{ scope.row[0] }}
							</router-link>
						</template>
					</el-table-column>
					<el-table-column prop="1" width="80" align="right" label="Posts" />
				</PaginatedTable>
			</el-col>
			<el-col :span="12">
				<PaginatedTable title="Locations by mood" icon="chart-line" :data="moodLocations">
					<el-table-column prop="0" label="Location">
						<template #default="scope">
							<router-link :to="{ name: 'timeline', query: { location: scope.row[0] } }">
								{{ scope.row[0] }}
							</router-link>
						</template>
					</el-table-column>
					<el-table-column prop="1" width="80" align="right" label="Ø Mood" />
				</PaginatedTable>
			</el-col>
		</EqualHeightRow>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { usePosts } from '@/stores/posts';
import EqualHeightRow from '@/components/EqualHeightRow.vue';
import PaginatedTable from '@/components/PaginatedTable.vue';

import Map from '@/components/Map';
import flow from 'lodash/fp/flow';
import filter from 'lodash/fp/filter';
import groupBy from 'lodash/fp/groupBy';
import pickBy from 'lodash/fp/pickBy';
import map from 'lodash/fp/map';
import sortBy from 'lodash/fp/sortBy';
import reverse from 'lodash/fp/reverse';
import toPairs from 'lodash/fp/toPairs';
import meanBy from 'lodash/meanBy';

const store = usePosts();
store.load();

const moodLocations = computed(() => {
	return flow(
		filter('location_verbose'),
		filter('mood'),
		groupBy('location_verbose'),
		pickBy((entries, _) => entries.length >= 5),
		toPairs,
		map(([location, entries]) => [location, meanBy(entries, (entry) => entry.mood).toPrecision(3)]),
		sortBy(1),
		reverse,
	)(store.postsList);
});

const postsGeojson = computed(() => {
	const geojson = {
		name: 'markers',
		type: 'FeatureCollection',
		features: [],
	};

	for (const post of store.postsList) {
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
});
</script>

<style lang="scss">
.locations {
	min-height: 100%;
	min-width: 100%;

	// Needed for EqualHeightRow with gutter
	overflow-x: hidden;
	overflow-x: clip;

	.locations-map {
		height: 600px;
		width: 100%;
		margin-bottom: 2rem;
	}
}
</style>
