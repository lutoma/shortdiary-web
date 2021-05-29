<template>
	<el-row class="post-timeline" :gutter="50">
		<el-col :span="19" class="left" v-loading="!posts.length">
			<template v-if="!posts.length">
				&nbsp;
			</template>

			<template v-if="posts.length && !sorted_posts.length">
				<h2>Could not find any posts matching your filters.</h2>
			</template>

			<div
				v-for="[year, months] of sorted_posts"
				:key="Number(year)"
				:id="`year-${year}`">

				<h1 class="year-header">{{ year }}</h1>

				<div
					ref="monthContainer"
					v-for="[month, posts] of months"
					:key="Number(`${year}${month}`)"
					:id="`month-${year}-${month}`"
					:data-year="year"
					:data-month="month">

					<h2 class="month-header">{{ getMonthName(month) }} <span>{{ year }}</span></h2>
					<div class="post-container" v-for="post in posts" :key="post.id">
						<Post :post="post" />
					</div>
				</div>
			</div>
		</el-col>

		<el-col :span="5" class="right">
			<slot name="sidebar"></slot>
			<div class="timeline-options">
				<ul class="datepicker">
					<li v-for="[year, months] of sorted_posts" :class="year == scroll_state.year ? 'active': ''" :key="Number(year)">
						<div @click="datePickerSelect" :data-scrolltarget="`#year-${year}`">{{ year }}</div>

						<ul v-show="year == scroll_state.year">
							<li
								v-for="[month, _] of months"
								:class="month == scroll_state.month ? 'active': ''"
								:data-scrolltarget="`#month-${year}-${month}`"
								@click="datePickerSelect"
								:key="Number(`${year}${month}`)">

								{{ getMonthName(month) }}
							</li>
						</ul>
					</li>
				</ul>

				<h2>Filters</h2>
				<el-form label-position="top" label-width="100px" :model="filter">
					<el-form-item>
						<el-input placeholder="Text" v-model="filter.text" clearable />
					</el-form-item>

					<el-form-item>
						<el-radio-group v-model="filter.image" size="small">
							<el-radio-button :label="null">Any</el-radio-button>
							<el-radio-button :label="true"><fa :icon="['far', 'images']" /> Has images</el-radio-button>
							<el-radio-button :label="false"><fa :icon="['far', 'empty-set']" /> No image</el-radio-button>
						</el-radio-group>
					</el-form-item>

					<el-form-item>
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

	async fetch() {
		await this.$store.dispatch('updatePosts')
	},

	data() {
		return {
			scroll_state: {
				observer_els: {},
				year: null,
				month: null
			},

			filter: {
				text: this.$route.query.filter || '',
				image: null,
				visibility: null,
				mood: [1, 10]
			}
		}
	},

	computed: {
		posts() {
			return this.$store.state.posts
		},

		sorted_posts() {
			let filtered = _(this.posts)
				.filter(x => x.text.toLowerCase().includes(this.filter.text.toLowerCase()))
				.filter(x => x.mood >= this.filter.mood[0] && x.mood <= this.filter.mood[1])

			if (this.filter.image !== null) {
				filtered = filtered.filter({ image: this.filter.image })
			}

			if (this.filter.visibility !== null) {
				filtered = filtered.filter({ public: this.filter.visibility === 'public' })
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

					return [x[0], mposts]
				})
				.value()
		}
	},

	methods: {
		getMonthName(num) {
			const date = new Date()
			date.setMonth(num - 1)
			return date.toLocaleString('en', { month: 'long' })
		},

		datePickerSelect(event) {
			const dest = document.querySelector(event.target.dataset.scrolltarget)

			// Cannot use ScrollIntoView here due to the abolute positioned
			// navbar that would cover up the heading
			if (dest) {
				window.scrollTo({ top: dest.offsetTop, left: 0, behavior: 'smooth' })
			}
		},

		intersectionCallback(update, observer) {
			// Handle IntersectionObserver callbacks. We need to store state
			// here to account for situations where two elements are visible at
			// once, and then later one of those goes out of view. The update
			// event in these cases will only list the element that has gone
			// out of view, but not the one that remains visible.

			// Turn into an Object for easier deduplication
			Object.assign(this.scroll_state.observer_els, _.keyBy(update, 'target.id'))

			const entries = Object.values(this.scroll_state.observer_els)
				.filter(x => x.isIntersecting)

			if (entries && entries.length) {
				this.scroll_state.year = entries[0].target.dataset.year
				this.scroll_state.month = entries[0].target.dataset.month
			}
		}
	},

	updated() {
		this.$nextTick(() => {
			const elements = this.$refs.monthContainer
			if (!elements) {
				return
			}

			const observer = new IntersectionObserver(this.intersectionCallback, {
				rootMargin: '-20% 0px 0px 0px'
				// threshold: [0, 0.25, 0.5, 0.75, 1]
			})

			for (const el of elements) {
				observer.observe(el)
			}
		})
	}
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

		.year-header {
			margin-bottom: 1rem;

			&:not(:first-of-type) {
				margin-top: 4rem;
			}
		}

		.month-header span {
			font-weight: 200;
		}

		.post-container {
			display: flex;
			flex-direction: row;
			margin: 35px 0;

			.post {
				flex-grow: 1;
			}
		}
	}

	.right {
		.timeline-options {
			position: sticky;
			top: 80px;
		}

		.el-radio-group {
			width: 100%;
			display: flex;
			flex-direction: row;

			.el-radio-button {
				flex: 1 1 33%;

				span {
					width: 100%;
				}
			}
		}

		.datepicker {
			margin: 0;
			padding: 0;
			margin-bottom: 2rem;

			> li {
				padding-left: 8px;
				margin-bottom: 4px;
				list-style-type: none;
				cursor: pointer;
				color: #036564;

				// Year display
				div {
					border-left: 4px solid #dedede;
					transition: border-left-color .3s;
					padding: .3rem .5rem;

					&:hover {
						border-left-color: #aeaeae;
						text-decoration: underline;
					}
				}

				// Sub-menu (months)
				ul {
					padding: 0;
					padding-left: 1rem;
					font-size: .95em;
					margin: .2rem 0;

					li {
						list-style-type: none;

						&.active {
							font-weight: 600;
						}
					}
				}

				&.active {
					div {
						border-left-color: #CDB380;
						font-weight: 700;
					}
				}
			}
		}
	}
}
</style>
