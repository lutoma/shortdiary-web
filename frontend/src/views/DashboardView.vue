<template>
	<div class="stats">
		<EqualHeightRow>
			<el-col :span="8">
				<PaginatedTableCard title="Frequent locations" icon="map-marked-alt" :data="store.locations">
					<el-table-column prop="0" label="Location">
						<template #default="scope">
							<router-link :to="{ name: 'timeline', query: { location: scope.row[0] } }">
								{{ scope.row[0] }}
							</router-link>
						</template>
					</el-table-column>
					<el-table-column prop="1" width="70" align="right" label="Posts" />
				</PaginatedTableCard>
			</el-col>
			<el-col :span="8">
				<PaginatedTableCard title="Frequent mentions" icon="users" :data="store.mentions">
					<el-table-column prop="0" label="Name">
						<template #default="scope">
							<router-link :to="{ name: 'timeline', query: { text: scope.row[0] } }">
								{{ scope.row[0] }}
							</router-link>
						</template>
					</el-table-column>
					<el-table-column prop="1" width="70" align="right" label="Posts" />
				</PaginatedTableCard>
			</el-col>
			<el-col :span="8">
				<PaginatedTableCard title="Locations by mood" icon="chart-line" :data="moodLocations">
					<el-table-column prop="0" label="Name" />
					<el-table-column prop="1" width="70" align="right" label="Mood" />
				</PaginatedTableCard>
			</el-col>
		</EqualHeightRow>

		<h2>Year to date</h2>
		<calendar-heatmap
			class="heatmap"
			:values="heatmap.values"
			:end-date="heatmap.endDate"
			tooltip-unit="chars"
			no-data-text="No post for this day"
			:range-color="['#f5f0e6', '#f5f0e6', '#e1d1b3', '#dccaa6', '#d7c299', '#d2bb8d', '#cdb380']"
		/>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import { usePosts } from '@/stores/posts';
import { CalendarHeatmap } from 'vue3-calendar-heatmap';
import EqualHeightRow from '@/components/EqualHeightRow.vue';
import PaginatedTableCard from '@/components/PaginatedTableCard.vue';

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

const heatmap = computed(() => {
	const now = new Date();
	const year = String(now.getFullYear());

	const values = flow(
		filter((x) => x.date.slice(0, 4) === year),
		map((x) => ({ date: x.date, count: x.text.length })),
	)(store.postsList);

	return {
		endDate: now.toISOString().slice(0, 10),
		values,
	};
});
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
		max-width: 1200px;

		svg {
			text {
				font-size: 8px;
			}
		}
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
