<template>
	<el-row class="post-timeline">
		<el-col :span="19" class="left" v-loading="!all_posts">
			<!-- v-infinite-scroll="loadPosts" -->
			<template v-if="!sorted_posts">
				&nbsp;
			</template>
			<template v-if="sorted_posts && !sorted_posts.length">
				Could not find any posts matching your filters.
			</template>
			<template v-for="[year, months] of sorted_posts">
				<h1 :id="`year-${year}`">{{ year }}</h1>
				<template v-for="[month, posts] of months">
					<h2>{{ getMonthName(month) }} {{ year }}</h2>
						<Post :post="post" v-for="post in posts" :key="post.id" />
					</el-timeline>
				</template>
			</template>
		</el-col>

		<el-col :span="5" class="right">
			<slot name="sidebar"></slot>
			<div class="timeline-options">
				<ul class='datepicker'>
					<li v-for="[year, _] of sorted_posts" :class="year == active_year ? 'active': ''" @click="datePickerSelect" :data-scrollto="year">
						<a :href="`#year-${year}`" :data-scrollto="year">{{ year }}</a>
					</li>
				</ul>

				<h2>Filters</h2>
				<el-form label-position="top" label-width="100px" :model="filter">
					<el-form-item label="Text">
						<el-input placeholder="Text" v-model="filter.text" />
					</el-form-item>

					<el-form-item>
						<el-switch v-model="filter.need_image" active-text="With image" />
					</el-form-item>

					<el-form-item label="Visibility">
						<el-radio-group v-model="filter.visibility" size="small">
							<el-radio-button :label="null">Any</el-radio-button>
							<el-radio-button label="public"><fa :icon="['far', 'lock-open']" /> Public</el-radio-button>
							<el-radio-button label="private"><fa :icon="['far', 'lock']" /> Private</el-radio-button>
						</el-radio-group>
					</el-form-item>

					<el-form-item label="Mood">
						<el-slider v-model="filter.mood" range show-stops :min="1" :max="10" :step="1" />
					</el-form-item>
				</el-form>
			</div>
		</el-col>
	</el-row>
</template>

<script>
import Post from '~/components/Post'
import _ from 'lodash'

export default {
	components: {
		Post
	},

	data() {
		return {
			all_posts: null,
			active_year: null,

			filter: {
				text: '',
				need_image: false,
				visibility: null,
				mood: [1, 10],
			}
		}
	},

	computed: {
		sorted_posts() {
			if(!this.all_posts) {
				return null
			}

			let filtered = _(this.all_posts)
				.filter(x => x.text.includes(this.filter.text))
				.filter(x => x.mood >= this.filter.mood[0] && x.mood <= this.filter.mood[1])

			if(this.filter.need_image) {
				filtered = filtered.filter('image')
			}

			if(this.filter.visibility) {
				filtered = filtered.filter({'public': this.filter.visibility === 'public'})
			}

			return filtered
				.groupBy(x => x.date.split('-')[0])
				.toPairs()
				.reverse()
				.map(x => {
					const mposts = _(x[1])
						.groupBy(y => y.date.split('-')[1])
						.toPairs()
						.value()

					return [x[0], mposts];
				})
				.value()
		}
	},

	async fetch() {
		this.all_posts = await this.$axios.$get('/posts/')
		//this.active_year = this.sorted_posts[0][0]
	},

	methods: {
		getMonthName(num) {
			return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][Number(num) - 1]
		},

		loadPosts() {
			console.log('loading new posts')
		},

		datePickerSelect(event) {
			const year = event.target.dataset.scrollto
			const dest = document.querySelector(`#year-${year}`)
			dest.scrollIntoView({ behavior: 'smooth' })
			this.active_year = year
		}
	},
}
</script>

<style lang="scss">
.post-timeline {
	height: 100%;
	display: flex;

	.el-loading-mask {
		background-color: transparent;
	}

	.left {
		height: 100%;

		padding-right: 3rem;

		.post {
			margin: 30px 0;
		}
	}

	.right {
		.timeline-options {
			position: sticky;
			top: 80px;
		}

		.datepicker {
			margin: 0;
			padding: 0;
			margin-bottom: 2rem;

			li {
				list-style-type: none;
				padding-left: 8px;
				margin-bottom: 4px;
				padding: 3px 8px;

				border-left: 4px solid #dedede;
				transition: border-left-color .3s;

				&:hover {
					border-left-color: #aeaeae;
				}

				&.active {
					border-left-color: #7e7e7e;
					font-weight: 600;
				}
			}
		}
	}
}
</style>
