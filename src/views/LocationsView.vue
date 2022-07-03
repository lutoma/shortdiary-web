<template>
	<div class="locations">
		<Map class="locations-map" :zoom="4" :geojson-cluster="postsGeojson" />
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { usePosts } from '@/stores/posts';
import Map from '@/components/Map';

const store = usePosts();
store.load();

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
