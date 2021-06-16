<template>
	<div class="post-timeline">
		<div class="filters">
			<h2>Filters</h2>
			<div class="filter-group">
				<el-popover placement="bottom" trigger="click">
					<el-button slot="reference"><fa :icon="['fal', 'align-left']" /> Text</el-button>
					<el-input placeholder="Text" v-model="filter.text" clearable />
				</el-popover>

				<el-popover placement="bottom" trigger="click">
					<el-button slot="reference"><fa :icon="['fal', 'shield-check']" /> Visibility</el-button>
					<el-radio-group v-model="filter.public" size="small">
						<el-radio-button :label="null">Any</el-radio-button>
						<el-radio-button :label="true"><fa :icon="['far', 'lock-open']" /> Public</el-radio-button>
						<el-radio-button :label="false"><fa :icon="['far', 'lock']" /> Private</el-radio-button>
					</el-radio-group>
				</el-popover>

				<el-popover placement="bottom" trigger="click">
					<el-button slot="reference"><fa :icon="['fal', 'smile']" /> Mood</el-button>
					<el-slider v-model="filter.mood" range show-stops :min="1" :max="10" :step="1" />
				</el-popover>

				<el-popover placement="bottom" trigger="click">
					<el-button slot="reference"><fa :icon="['fal', 'tags']" /> Tags</el-button>
					<el-select v-model="filter.tags" multiple filterable default-first-option placeholder="Choose tags">
						<el-option v-for="item in top_tags" :key="item[0]" :label="item[0]" :value="item[0]" />
					</el-select>
				</el-popover>

				<el-popover placement="bottom" trigger="click">
					<el-button slot="reference"><fa :icon="['fal', 'map-marked-alt']" /> Location</el-button>
					<el-select v-model="filter.location" placeholder="Select location" filterable clearable>
						<el-option v-for="item in top_locations" :key="item[0]" :label="item[0]" :value="item[0]" />
					</el-select>
				</el-popover>

				<el-popover placement="bottom" trigger="click">
					<el-button slot="reference"><fa :icon="['fal', 'images']" /> Images</el-button>
					<el-radio-group v-model="filter.images" size="small">
						<el-radio-button :label="null">Any</el-radio-button>
						<el-radio-button :label="true"><fa :icon="['far', 'images']" /> Has images</el-radio-button>
						<el-radio-button :label="false"><fa :icon="['far', 'empty-set']" /> No image</el-radio-button>
					</el-radio-group>
				</el-popover>
			</div>
		</div>

		<div class="timeline-main">
			<div class="posts" v-loading="!posts.length">
				<template v-if="!posts.length">
					&nbsp;
				</template>

				<template v-if="posts.length && !sorted_posts.length">
					<h2>Could not find any posts matching your filters.</h2>
				</template>

				<section
					v-for="[year, months] of sorted_posts"
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

						<h2 class="month-header">{{ getMonthName(month) }}</span></h2>
						<div class="post-container" v-for="post in posts" :key="post.id">
							<div class="post-date">
								<h3>{{ post.date.split('-')[2] }}</h3>
								<div class="weekday">{{ new Date(post.date).toLocaleString('en',  { weekday: 'long' }) }}</div>
							</div>
							<Post :post="post" :show-date="false" @deleted="loadPosts()" />
						</div>
					</section>
				</section>
			</div>

			<nav class="datepicker">
				<ul>
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
			</nav>
		</div>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import Post from '~/components/Post'
import _ from 'lodash'

export default {
	components: {
		Post
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
				public: null,
				mood: [1, 10],
				tags: [],
				location: null,
				images: null
			}
		}
	},

	computed: {
		...mapState(['posts', 'top_locations', 'top_tags']),

		sorted_posts() {
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

			// Now, group the filtered posts into years and months for display
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
		async loadPosts() {
			await this.$store.dispatch('updatePosts')
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

	async fetch() {
		await this.loadPosts()
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
	},

	watch: {
		// Watch for route changes since the component query parameters can
		// change when a user clicks on a @mention in a post (appending
		// ?filter=@mention etc. to the URL).
		$route (to, from) {
			this.filter.text = to.query.filter || ''
		}
	}
}
</script>

<style lang="scss">
$date-aside-margin: 30px;
$date-aside-width: 130px;

.post-timeline {
	height: 100%;

	.el-loading-mask {
		background-color: transparent;
	}

	// Arrange filter buttons into a button-group of sorts.
	// el-button-group is incompatible with el-popover
	.filters {
		margin-bottom: 2rem;
		margin-left: $date-aside-width + $date-aside-margin;

		display: flex;
		flex-direction: row;

		// Needs to be above .timeline-main which is pulled up by negative margin
		//position: relative;
		//z-index: 30;

		h2 {
			margin-right: 1rem;
			margin-bottom: 0;
		}

		.filter-group {
			display: flex;
			flex-direction: row;

			> span {
				display: block;

				&:not(:first-of-type) {
					.el-button {
						border-left: 0;
						border-top-left-radius: 0;
						border-bottom-left-radius: 0;
					}
				}

				&:not(:last-of-type) {
					.el-button {
						border-top-right-radius: 0;
						border-bottom-right-radius: 0;
					}
				}
			}

			.el-select {
				width: 100%;
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
		}
	}

	.timeline-main {
		display: flex;
		//margin-top: -80px;
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

	.datepicker {
		flex: 0.1 0 150px;

		> ul {
			// This was originally position: sticky, but Firefox has
			// performance issues/flickering with that. See:
			// https://bugzilla.mozilla.org/show_bug.cgi?id=1585378
			position: fixed;
			top: 90px;

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
