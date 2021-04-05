<template>
	<div class="stats">
		<Map style="height: 350px" zoom="4" />

		<div id="main-container">
			<h1>Stats</h1>

			<!--<calendar-heatmap :values="[{ date: '2021-3-22', count: 6 }]" :end-date="2021-3-30" />-->

			<PostLengthChart :chart-data="{labels: ['January', 'February'], datasets: [{label: 'Data One', backgroundColor: '#f87979', data: [40, 20]}]}" :options="{responsive: true, maintainAspectRatio: false}" height="200" />

			<el-row :gutter="50">
				<el-col :span="8">
					<h2>Frequent locations</h2>
					<el-table
					:data="frequent_locations"
					stripe
					style="width: 100%">
						<el-table-column prop="rank" width="35" label="#" />
						<el-table-column prop="name" label="Location" />
						<el-table-column prop="num_posts" width="70" label="Posts" />
					</el-table>
				</el-col>
				<el-col :span="8">
					<h2>Frequently mentioned</h2>
					<el-table
					:data="frequent_locations"
					stripe
					style="width: 100%">
						<el-table-column prop="rank" width="35" label="#" />
						<el-table-column prop="name" label="Name" />
						<el-table-column prop="num_posts" width="70" label="Posts" />
					</el-table>
				</el-col>
				<el-col :span="8">
					<h2>Locations by avg. mood</h2>
					<el-table
					:data="frequent_locations"
					stripe
					style="width: 100%">
						<el-table-column prop="rank" width="35" label="#" />
						<el-table-column prop="name" label="Name" />
						<el-table-column prop="num_posts" width="70" label="Mood" />
					</el-table>
				</el-col>
			</el-row>
		</div>
	</div>
</template>

<script>
//import CalendarHeatmap from 'vue-calendar-heatmap'
import Map from '~/components/Map'
import PostLengthChart from '~/components/PostLengthChart'

export default {
	layout: 'no-container',
	components: {
		Map,
		//CalendarHeatmap,
		PostLengthChart
	},
	data() {
		return {
			frequent_locations: [
				{rank: 1, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 2, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 3, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 4, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 5, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 6, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 7, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 8, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 9, name: 'Mannheim, Germany', num_posts: 123},
				{rank: 10, name: 'Mannheim, Germany', num_posts: 123}
			]
		}
	}
}
</script>

<style lang="scss">
.stats {
	// Needed to push footer down. Usually done by main containerm, but we use
	// the no-container layout here
	flex-grow: 1;
}
</style>
