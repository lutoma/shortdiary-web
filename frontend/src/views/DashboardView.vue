<template>
	<div class="stats">
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
						<template v-slot="scope">
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

		<h2>Year to date</h2>
		<!--<calendar-heatmap class="heatmap" :values="heatmap.values" :end-date="heatmap.endDate" />-->
		<!--<PostLengthChart style="margin-top: 4rem;" :chart-data="{labels: ['January', 'February'], datasets: [{label: 'Data One', backgroundColor: '#f87979', data: [40, 20]}]}" :options="{responsive: true, maintainAspectRatio: false}" :height="200" />-->
	</div>
</template>

<script>
import { mapState } from 'pinia';
import { usePosts } from '@/stores/posts';
import { CalendarHeatmap } from 'vue3-calendar-heatmap';
import PostLengthChart from '@/components/PostLengthChart.js';
import EqualHeightRow from '@/components/EqualHeightRow.vue';
import PaginatedTableCard from '@/components/PaginatedTableCard.vue';
import PostTimeline from '@/components/PostTimeline.vue';
import Map from '@/components/Map';
import _ from 'lodash';

export default {
	// layout: 'no-container',
	components: {
		CalendarHeatmap,
		PostLengthChart,
		EqualHeightRow,
		PaginatedTableCard,
		Map,
		PostTimeline,
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

		heatmap() {
			const now = new Date();
			const year = String(now.getFullYear());

			const values = _(this.posts)
				.filter((x) => x.date.slice(0, 4) === year)
				.map((x) => ({ date: x.date, count: x.text.length }))
				.value();

			return {
				endDate: now.toISOString().slice(0, 10),
				values,
			};
		},
	},

	head() {
		return { title: 'Stats – shortdiary' };
	},
};
</script>

<style lang="scss">
.stats {
	// Needed to push footer down. Usually done by main containerm, but we use
	// the no-container layout here
	flex-grow: 1;

	.stats-map {
		min-height: 250px;
		max-height: 400px;
		height: 30vh;
	}

	.heatmap {
		margin: 1rem;
		margin-bottom: 3rem;
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
