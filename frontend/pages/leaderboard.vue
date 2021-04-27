<template>
	<div>
		<h1>Leaderboard</h1>

		<el-row :gutter="50">
			<el-col :span="8">
				<h2>Number of posts</h2>
				<el-table
					v-loading="!leaderboard"
					:data="leaderboard.number_of_posts"
					stripe
					style="width: 100%">

					<el-table-column prop="username" label="Username" />
					<el-table-column prop="num_posts" width="70" label="Posts" />
				</el-table>
			</el-col>

			<el-col :span="8">
				<h2>Average post length</h2>
				<el-table
					v-loading="!leaderboard"
					:data="leaderboard.average_post_length"
					stripe
					style="width: 100%">

					<el-table-column prop="username" label="Username" />
					<el-table-column prop="avg_length" width="120" label="Chars" />
				</el-table>
			</el-col>

			<el-col :span="8">
				<h2>Longest current streak</h2>
				<el-table
					v-loading="!leaderboard"
					:data="leaderboard.longest_current_streak"
					stripe
					style="width: 100%">

					<el-table-column prop="username" label="Username" />
					<el-table-column prop="streak" width="70" label="Days" />
				</el-table>
			</el-col>
		</el-row>
	</div>
</template>

<script>
export default {
	data() {
		return {
			leaderboard: {
				number_of_posts: [],
				average_post_length: [],
				longest_current_streak: []
			}
		}
	},

	async fetch() {
		this.leaderboard = await this.$axios.$get('/leaderboard/')
	}
}
</script>
