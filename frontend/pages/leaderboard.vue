<template>
	<div class="leaderboard">
		<h1>Leaderboard</h1>

		<EqualHeightRow>
			<el-col :span="8">
				<el-card>
					<h2>Longest current streak</h2>
					<el-table
						v-loading="!leaderboard.longest_current_streak.length"
						:data="leaderboard.longest_current_streak"
						stripe
						style="width: 100%">

						<el-table-column prop="username" label="Username" />
						<el-table-column prop="streak" width="70" align="right" label="Days" />
					</el-table>
				</el-card>
			</el-col>

			<el-col :span="8">
				<el-card>
					<h2>Number of posts</h2>
					<el-table
						v-loading="!leaderboard.number_of_posts.length"
						:data="leaderboard.number_of_posts"
						stripe
						style="width: 100%">

						<el-table-column prop="username" label="Username" />
						<el-table-column prop="num_posts" width="70" align="right" label="Posts" />
					</el-table>
				</el-card>
			</el-col>

			<el-col :span="8">
				<el-card>
					<h2>Average post length</h2>
					<el-table
						v-loading="!leaderboard.average_post_length.length"
						:data="leaderboard.average_post_length"
						stripe
						style="width: 100%">

						<el-table-column prop="username" label="Username" />
						<el-table-column prop="avg_length" width="70" align="right" label="Chars" />
					</el-table>
				</el-card>
			</el-col>

			<el-col :span="8">
				<el-card>
					<h2><fa :icon="['fal', 'language']" /> Popular languages</h2>
					<el-table
						v-loading="!leaderboard.popular_languages.length"
						:data="leaderboard.popular_languages"
						stripe
						style="width: 100%">

						<el-table-column prop="language" label="Language" />
						<el-table-column prop="num_posts" width="70" align="right" label="Posts" />
					</el-table>
				</el-card>
			</el-col>

			<el-col :span="8">
				<el-card>
					<h2><fa :icon="['fal', 'map-marked-alt']" /> Popular locations</h2>
					<el-table
						v-loading="!leaderboard.popular_locations.length"
						:data="leaderboard.popular_locations"
						stripe
						style="width: 100%">

						<el-table-column prop="location_verbose" label="Location" />
						<el-table-column prop="num_posts" width="70" align="right" label="Posts" />
					</el-table>
				</el-card>
			</el-col>
		</EqualHeightRow>

		<p><small>Updated every five minutes. Last update: {{ leaderboard.last_update }}</small></p>
	</div>
</template>

<script>
import EqualHeightRow from '~/components/EqualHeightRow'

export default {
	components: {
		EqualHeightRow
	},
	data() {
		return {
			leaderboard: {
				number_of_posts: [],
				average_post_length: [],
				longest_current_streak: [],
				popular_languages: [],
				popular_locations: []
			}
		}
	},

	async fetch() {
		this.leaderboard = await this.$axios.$get('/leaderboard/')
	},

	head () {
		return { title: 'Leaderboard – shortdiary' }
	}
}
</script>

<style lang="scss">
.leaderboard {
	.el-row {
		margin-bottom: 3rem;
	}

	.el-col {

	}
}
</style>
