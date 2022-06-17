<template>
	<div class="post-timeline">
		<div class="posts" v-loading="!posts.length">
			<template v-if="!posts.length">
				&nbsp;
			</template>

			<template v-if="posts.length && !grouped_posts.length">
				<h2>Could not find any posts matching your filters.</h2>
			</template>

			<section
				v-for="[year, months] of grouped_posts"
				:key="Number(year)"
				:id="`year-${year}`">

				<h1 class="year-header">{{ year }}</h1>

				<section
					ref="monthContainer"
					v-for="[month, posts] of months"
					:key="Number(`${year}${month}`)"
					:id="`month-${year}-${month}`"
					:data-year="year"
					:data-month="month">

					<h2 class="month-header">{{ getMonthName(month) }}</h2>
					<div class="post-container" v-for="post in posts" :key="post.id">
						<div class="post-date">
							<h3>{{ post.date.split('-')[2] }}</h3>
							<div class="weekday">{{ new Date(post.date).toLocaleString('en',  { weekday: 'long' }) }}</div>
						</div>
						<Post ref="posts" :post="post" :show-date="false" @deleted="loadPosts()" />
					</div>
				</section>
			</section>
		</div>

		<nav>
			<div>
				<ol class="datepicker">
					<li
						v-for="[year, months] of datepicker_values"
						:class="year == scroll_state.year ? 'active': ''" :key="Number(year)">

						<div @click="datePickerSelect" :data-scrolltarget="`#year-${year}`">{{ year }}</div>

						<ol v-show="year == scroll_state.year">
							<li
								v-for="[month, _] of months"
								:class="month == scroll_state.month ? 'active': ''"
								:data-scrolltarget="`#month-${year}-${month}`"
								@click="datePickerSelect"
								:key="Number(`${year}${month}`)">

								{{ getMonthName(month) }}
							</li>
						</ol>
					</li>
				</ol>

				<h2>Filters</h2>
				<ol class="filters">
					<li>
						<fa :icon="['fal', 'align-left']" />
						<el-input placeholder="Text" v-model="filter.text" clearable />
					</li>

					<li>
						<fa :icon="['fal', 'smile']" />
						<el-slider v-model="filter.mood" range show-stops :min="1" :max="10" :step="1" />
					</li>

					<li>
						<fa :icon="['fal', 'tags']" />
						<el-select v-model="filter.tags" multiple filterable default-first-option placeholder="Choose tags">
							<el-option v-for="item in top_tags" :key="item[0]" :label="item[0]" :value="item[0]" />
						</el-select>
					</li>

					<li>
						<fa :icon="['fal', 'map-marked-alt']" />
						<el-select v-model="filter.location" placeholder="Select location" filterable clearable>
							<el-option label="" :value="null">Any</el-option>
							<el-option v-for="item in top_locations" :key="item[0]" :label="item[0]" :value="item[0]" />
						</el-select>
					</li>

					<li>
						<fa :icon="['fal', 'images']" />
						<el-select v-model="filter.images" placeholder="Images" filterable clearable>
							<el-option label="" :value="null">Any</el-option>
							<el-option label="No images" :value="false" />
							<el-option label="Has images" :value="true" />
						</el-select>
					</li>
				</ol>
			</div>
		</nav>
	</div>
</template>

<script>
import { mapState } from 'pinia'
import { usePosts } from '@/stores/posts';
import Post from '@/components/Post.vue'
import _ from 'lodash'

export default {
	components: {
		Post
	},

	setup() {
		const store = usePosts();
		store.load();
	},

	data() {
		return {
			infinite_scroll: {
				observer: null,
				state: false
			},

			scroll_state: {
				observer_els: {},
				year: null,
				month: null
			},

			filter: {
				text: this.$route.query.filter || '',
				public: null,
				mood: [1, 10],
				tags: [],
				location: null,
				images: null
			},

			visible_posts: 10
		}
	},

	computed: {
		...mapState(usePosts, ['posts', 'top_tags', 'top_locations']),

		filtered_posts() {
			// Filter definitions. The object key defines the field in
			// this.filter that will be checked to see if filtering is
			// necessary, the value contains the function or object that gets
			// passed to .filter
			const filters = {
				text: post => post.text.toLowerCase().includes(this.filter.text.toLowerCase()),
				public: { public: this.filter.public },
				tags: post => post.tags.some(tag => this.filter.tags.includes(tag)),
				location: { location_verbose: this.filter.location },
				images: post => !!post.images.length === this.filter.images
			}

			let filtered = _(this.posts)
				.filter(x => x.mood >= this.filter.mood[0] && x.mood <= this.filter.mood[1])

			for (const [cond, filter] of Object.entries(filters)) {
				const value = this.filter[cond]

				if (value !== null && value !== '' && (typeof value !== 'object' || value.length)) {
					filtered = filtered.filter(filter)
				}
			}

			return filtered
		},

		grouped_posts() {
			// Group the filtered posts into years and months for display
			return this.filtered_posts
				.slice(0, this.visible_posts)
				.groupBy(x => x.date.split('-')[0])
				.toPairs()
				.reverse()
				.map(x => {
					const mposts = _(x[1])
						.groupBy(y => y.date.split('-')[1])
						.toPairs()
						.orderBy((p) => p[0], 'desc')
						.value()

					return [x[0], mposts]
				})
				.value()
		},

		datepicker_values() {
			// Essentially the same as grouped_posts, but without the slicing
			// for infinite loading. It would be much nicer to deduplicate
			// this somehow, but slicing after grouping is nontrivial.

			return this.filtered_posts
				.groupBy(x => x.date.split('-')[0])
				.toPairs()
				.reverse()
				.map(x => {
					const mposts = _(x[1])
						.groupBy(y => y.date.split('-')[1])
						.toPairs()
						.orderBy((p) => p[0], 'desc')
						.value()

					return [x[0], mposts]
				})
				.value()
		}
	},

	methods: {
		async loadPosts() {
			const store = usePosts();
			store.load();
		},

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

		updateInfiniteScrollObserver() {
			this.infinite_scroll.observer.disconnect()
			this.infinite_scroll.observer.observe(this.$refs.posts.slice(-1)[0].$el)
		},

		infiniteScrollCallback(update, observer) {
			const new_state = update[0].isIntersecting
			if (!this.infinite_scroll.state && new_state) {
				this.infinite_scroll.state = true
				this.visible_posts += 10
				this.updateInfiniteScrollObserver()
			} else {
				this.infinite_scroll.state = new_state
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
			// Set up IntersectionObserver for infinite scrolling
			this.infinite_scroll.observer = new IntersectionObserver(this.infiniteScrollCallback)
			this.updateInfiniteScrollObserver()

			// Set up IntersectionObserver for datepicker
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
	},

	watch: {
		// Watch for route changes since the component query parameters can
		// change when a user clicks on a @mention in a post (appending
		// ?filter=@mention etc. to the URL).
		$route (to, from) {
			this.filter.text = to.query.filter || ''
		},

		// Reset infinite scrolling and scroll back to top on filter
		filter: {
			deep: true,

			handler(val) {
				window.scrollTo({ top: 0, left: 0 })
				this.visible_posts = 10
			}
		}
	}
}
</script>

<style lang="scss">
$date-aside-margin: 30px;
$date-aside-width: 130px;

.post-timeline {
	height: 100%;
	display: flex;

	.el-loading-mask {
		background-color: transparent;
	}

	.posts {
		height: 100%;
		flex: 1 1 100%;
		margin-right: 40px;

		.year-header {
			position: sticky;
			top: 50px;

			width: $date-aside-width;
			text-align: right;

			// To keep alignment consistent with absolute/sticky positioning
			margin: 0;
			height: 60px;

			background: #F9F9F9;

			// Position above month-header
			z-index: 10;

			padding-top: 20px;
			margin-top: -30px;
		}

		.month-header {
			position: sticky;
			top: 110px;
			margin: 0;

			width: $date-aside-width;
			text-align: right;

			background: #F9F9F9;

			// Position below year-header
			z-index: 9;

			padding-bottom: 15px;
			margin-bottom: -15px;
			//box-shadow: 0 30px 40px rgba(0,0,0,.1);
		}

		.post-container {
			display: flex;
			flex-direction: row;
			margin: 35px 0;

			.post-date {
				flex: 0 0 $date-aside-width;
				margin-right: $date-aside-margin;
				text-align: right;
				padding-top: 10px;

				h3 {
					font-size: 1.5rem;
					font-weight: 700;
					margin-bottom: .5rem;
				}

				.weekday {
					font-weight: 200;
				}
			}

			.post {
				flex: 1 1 auto;
			}
		}
	}

	nav {
		flex: 0.1 0 275px;

		> div {
			// This was originally position: sticky, but Firefox has
			// performance issues/flickering with that. See:
			// https://bugzilla.mozilla.org/show_bug.cgi?id=1585378
			position: fixed;
			top: 90px;
			width: 275px;
		}

		ol.datepicker {
			margin: 0;
			padding: 0;
			margin-bottom: 3rem;

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
				ol {
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

		.filters {
			list-style-type: none;
			margin: 0;
			padding: 0;
			margin-top: 1rem;

			> li {
				margin-bottom: 1rem;
				display: flex;
				flex-direction: row;
				align-items: center;

				svg {
					flex: 0 0 20px;
					min-width: 20px;
					margin-right: .75rem;
				}

				.el-select, .el-radio-group, .el-input, .el-slider {
					width: 100%;
				}

				.el-slider {
					padding: 0 8px;
				}
			}
		}
	}
}
</style>
