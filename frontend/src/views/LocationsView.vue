<template>
	<div class="locations">
		<Map class="stats-map" :zoom="4" :geojson-cluster="posts_geojson" />

		<div id="main-container">
			<h1>Locations</h1>

			<EqualHeightRow>
				<el-col :span="8">
					<PaginatedTableCard title="Frequent locations" icon="map-marked-alt" :data="top_locations">
						<el-table-column prop="0" label="Location" />
						<el-table-column prop="1" width="70" align="right" label="Posts" />
					</PaginatedTableCard>
				</el-col>
				<el-col :span="8">
					<PaginatedTableCard title="Frequent mentions" icon="users" :data="top_mentions">
						<el-table-column prop="0" label="Name">
							<template slot-scope="scope">
								<n-link :to="`/dashboard?filter=${scope.row[0]}`">{{ scope.row[0] }}</n-link>
							</template>
						</el-table-column>
						<el-table-column prop="1" width="70" align="right" label="Posts" />
					</PaginatedTableCard>
				</el-col>
				<el-col :span="8">
					<PaginatedTableCard title="Locations by mood" icon="chart-line" :data="top_mood_locations">
						<el-table-column prop="0" label="Name" />
						<el-table-column prop="1" width="70" align="right" label="Mood" />
					</PaginatedTableCard>
				</el-col>
			</EqualHeightRow>
		</div>
	</div>
</template>

<script>
import { mapState } from 'pinia'
import { usePosts } from '@/stores/posts';
import PostLengthChart from '@/components/PostLengthChart.js'
import EqualHeightRow from '@/components/EqualHeightRow.vue'
import PaginatedTableCard from '@/components/PaginatedTableCard.vue'
import Map from '@/components/Map'
import _ from 'lodash'

export default {
	//layout: 'no-container',
	components: {
		PostLengthChart,
		EqualHeightRow,
		PaginatedTableCard,
		Map
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
			time_frame: 'all'
		}
	},

	computed: {
		...mapState(usePosts, ['posts', 'top_locations', 'top_mentions']),

		top_mood_locations() {
			return _(this.posts)
				.filter('location_verbose')
				.filter('mood')
				.groupBy('location_verbose')
				.pickBy((entries, _) => entries.length >= 5)
				.map((entries, location) => [location, _.meanBy(entries, entry => entry.mood).toPrecision(3)])
				.sortBy(1)
				.reverse()
				.value()
		},

		posts_geojson() {
			const geojson = {
				name: 'markers',
				type: 'FeatureCollection',
				features: []
			}

			for (const post of this.posts) {
				if (!post.location_lon || !post.location_lat) {
					continue
				}

				geojson.features.push({
					type: 'Feature',
					properties: { label: `<a href="/posts/${post.id}">${post.date}</a>` },
					geometry: {
						type: 'Point',
						coordinates: [post.location_lon, post.location_lat]
					}
				})
			}

			return geojson
		},

	},

	head () {
		return { title: 'Stats – shortdiary' }
	}
}
</script>

<style lang="scss">
.locations {
	// Needed to push footer down. Usually done by main containerm, but we use
	// the no-container layout here
	flex-grow: 1;

	.stats-map {
		min-height: 250px;
		max-height: 400px;
		height: 30vh;
	}

	.card-table-row {
		margin-bottom: 3rem;
	}

	.el-pagination {
		margin-top: 1rem;
		display: flex;

		.el-pager {
			flex-grow: 1;
			text-align: center;
		}
	}
}
</style>
