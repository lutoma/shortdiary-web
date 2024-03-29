<template>
	<div class="post-timeline">
		<div v-loading="!store.loaded" class="posts">
			<router-link class="new-entry-button" :to="{ name: 'new-post' }">
				<el-button type="primary">
					<fa :icon="['far', 'file-plus']" /> New entry
				</el-button>
			</router-link>
			<template v-if="!store.posts.size">
				&nbsp;
			</template>

			<template v-if="store.posts.size && !groupedPosts.length">
				<h2>Could not find any posts matching your filters.</h2>
			</template>

			<section
				v-for="[year, months] of groupedPosts"
				:id="`year-${year}`"
				:key="Number(year)"
			>
				<h1 class="year-header">
					{{ year }}
				</h1>

				<section
					v-for="[month, posts] of months"
					:id="`month-${year}-${month}`"
					ref="monthContainer"
					:key="Number(`${year}${month}`)"
					:data-year="year"
					:data-month="month"
				>
					<h2 class="month-header">
						{{ getMonthName(month) }}
					</h2>
					<div v-for="post in posts" :key="post.id" class="post-container">
						<div class="post-date">
							<h3>{{ post.date.split('-')[2] }}</h3>
							<div class="weekday">
								{{ new Date(post.date).toLocaleString('en', { weekday: 'long' }) }}
							</div>
						</div>
						<Post ref="postElements" :post="post" :show-date="false" />
					</div>
				</section>
			</section>
		</div>

		<nav>
			<div>
				<ol class="datepicker">
					<li
						v-for="[year, months] of datepickerValues"
						:key="Number(year)" :class="year == scrollState.year ? 'active': ''"
					>
						<div :data-scrolltarget="`#year-${year}`" @click="datePickerSelect">
							{{ year }}
						</div>

						<ol v-show="year == scrollState.year">
							<li
								v-for="[month, _unused] of months"
								:key="Number(`${year}${month}`)"
								:class="month == scrollState.month ? 'active': ''"
								:data-scrolltarget="`#month-${year}-${month}`"
								@click="datePickerSelect"
							>
								{{ getMonthName(month) }}
							</li>
						</ol>
					</li>
				</ol>

				<h2 class="filters-heading">Filters</h2>
				<ol class="filters">
					<li>
						<fa :icon="['fal', 'align-left']" />
						<el-input v-model="setFilters.text" placeholder="Text" clearable />
					</li>

					<li>
						<fa :icon="['fal', 'smile']" />
						<el-slider v-model="setFilters.mood" range show-stops :min="1" :max="10" :step="1" />
					</li>

					<li>
						<fa :icon="['fal', 'tags']" />
						<el-select v-model="setFilters.tags" multiple filterable default-first-option placeholder="Choose tags">
							<el-option v-for="item in store.tags" :key="item[0]" :label="item[0]" :value="item[0]" />
						</el-select>
					</li>

					<li>
						<fa :icon="['fal', 'map-marked-alt']" />
						<el-select v-model="setFilters.location" placeholder="Select location" filterable clearable>
							<el-option label="" :value="null">
								Any
							</el-option>
							<el-option v-for="item in store.locations" :key="item[0]" :label="item[0]" :value="item[0]" />
						</el-select>
					</li>

					<li>
						<fa :icon="['fal', 'images']" />
						<el-select v-model="setFilters.images" placeholder="Images" filterable clearable>
							<el-option label="" :value="null">
								Any
							</el-option>
							<el-option label="No images" :value="false" />
							<el-option label="Has images" :value="true" />
						</el-select>
					</li>
				</ol>
			</div>
		</nav>
	</div>
</template>

<script setup>
import {
	ref, reactive, computed, onUpdated,
} from 'vue';

import flow from 'lodash/fp/flow';
import filter from 'lodash/fp/filter';
import slice from 'lodash/fp/slice';
import groupBy from 'lodash/fp/groupBy';
import toPairs from 'lodash/fp/toPairs';
import reverse from 'lodash/fp/reverse';
import map from 'lodash/fp/map';
import orderBy from 'lodash/fp/orderBy';
import keyBy from 'lodash/keyBy';

import { useQuery } from '@oarepo/vue-query-synchronizer';
import { usePosts } from '@/stores/posts';
import Post from '@/components/Post.vue';

const store = usePosts();
const setFilters = useQuery();
store.load();

const visiblePosts = ref(10);
const filteredPosts = computed(() => {
	// Filter definitions. The object key defines the field in
	// filter that will be checked to see if filtering is
	// necessary, the value contains the function or object that gets
	// passed to .filter
	const filters = {
		text: (post) => post.text.toLowerCase().includes(setFilters.text.toLowerCase()),
		tags: (post) => post.tags.some((tag) => setFilters.tags.includes(tag)),
		location: { location_verbose: setFilters.location },
		images: (post) => !!post.images.length === setFilters.images,
	};

	const flowFilters = [];
	for (const [cond, nfilter] of Object.entries(filters)) {
		const value = setFilters[cond];

		if (value !== '' && value !== null && value !== 'null' && (typeof value !== 'object' || value.length)) {
			flowFilters.push(filter(nfilter));
		}
	}

	// FIXME return unprocessed flow
	return flow(
		filter((x) => x.mood >= Number(setFilters.mood[0]) && x.mood <= Number(setFilters.mood[1])),
		...flowFilters,
	)(store.postsList);
});

const groupedPosts = computed(() => {
	// Group the filtered posts into years and months for display

	return flow(
		slice(0, visiblePosts.value),
		groupBy((x) => x.date.split('-')[0]),
		toPairs,
		reverse,
		map((x) => {
			const mposts = flow(
				groupBy((y) => y.date.split('-')[1]),
				toPairs,
				orderBy((p) => p[0], 'desc'),
			)(x[1]);

			return [x[0], mposts];
		}),
	)(filteredPosts.value);
});

const datepickerValues = computed(() => {
	// Essentially the same as groupedPosts, but without the slicing
	// for infinite loading. It would be much nicer to deduplicate
	// this somehow, but slicing after grouping is nontrivial.

	return flow(
		groupBy((x) => x.date.split('-')[0]),
		toPairs,
		reverse,
		map((x) => {
			const mposts = flow(
				groupBy((y) => y.date.split('-')[1]),
				toPairs,
				orderBy((p) => p[0], 'desc'),
			)(x[1]);

			return [x[0], mposts];
		}),
	)(filteredPosts.value);
});

const infiniteScroll = reactive({
	observer: null,
	state: false,
});

const scrollState = reactive({
	observer_els: {},
	year: null,
	month: null,
});

const postElements = ref();
function updateInfiniteScrollObserver() {
	infiniteScroll.observer.disconnect();
	const els = postElements.value;

	if (els && els.length) {
		infiniteScroll.observer.observe(els.slice(-1)[0].$el);
	}
}

function infiniteScrollCallback(update, _) {
	const newState = update[0].isIntersecting;
	if (!infiniteScroll.state && newState) {
		infiniteScroll.state = true;
		visiblePosts.value += 10;
		updateInfiniteScrollObserver();
	} else {
		infiniteScroll.state = newState;
	}
}

function intersectionCallback(update, _unused) {
	// Handle IntersectionObserver callbacks. We need to store state
	// here to account for situations where two elements are visible at
	// once, and then later one of those goes out of view. The update
	// event in these cases will only list the element that has gone
	// out of view, but not the one that remains visible.

	// Turn into an Object for easier deduplication
	Object.assign(scrollState.observer_els, keyBy(update, 'target.id'));

	const entries = Object.values(scrollState.observer_els)
		.filter((x) => x.isIntersecting);

	if (entries && entries.length) {
		scrollState.year = entries[0].target.dataset.year;
		scrollState.month = entries[0].target.dataset.month;
	}
}

const monthContainer = ref();
onUpdated(() => {
	// Set up IntersectionObserver for infinite scrolling
	infiniteScroll.observer = new IntersectionObserver(infiniteScrollCallback);
	updateInfiniteScrollObserver();

	// Set up IntersectionObserver for datepicker
	const elements = monthContainer.value;
	if (!elements) {
		return;
	}

	const observer = new IntersectionObserver(intersectionCallback, {
		rootMargin: '-20% 0px 0px 0px',
		// threshold: [0, 0.25, 0.5, 0.75, 1]
	});

	for (const el of elements) {
		observer.observe(el);
	}
});

function getMonthName(num) {
	const date = new Date();
	date.setMonth(num - 1);
	return date.toLocaleString('en', { month: 'long' });
}

function datePickerSelect(event) {
	let dest = document.querySelector(event.target.dataset.scrolltarget);

	if (dest) {
		window.scrollTo({ top: dest.offsetTop, left: 0, behavior: 'smooth' });
	} else {
		console.log('datepicker no dest, loading', visiblePosts.value, store.posts.size);
		while (visiblePosts.value < store.posts.size && !document.querySelector(event.target.dataset.scrolltarget)) {
			visiblePosts.value += 10;
			console.log('visible', visiblePosts.value);
		}

		setTimeout(() => {
			dest = document.querySelector(event.target.dataset.scrolltarget);
			console.log('dest now', dest);

			if (dest) {
				window.scrollTo({ top: dest.offsetTop, left: 0, behavior: 'smooth' });
			}
		}, 1);
	}
}
</script>

<style lang="scss">
$date-aside-margin: 30px;
$date-aside-width: 100px;

.post-timeline {
	display: flex;
	flex-grow: 1;

	.el-loading-mask {
		background-color: transparent;
	}

	.posts {
		height: 100%;
		flex: 1 1 100%;
		margin-right: 40px;

		.new-entry-button {
			float: right;
		}

		.year-header {
			position: sticky;
			top: 0px;

			width: $date-aside-width;
			text-align: right;

			// To keep alignment consistent with absolute/sticky positioning
			margin: 0;
			height: 60px;

			font-size: 1.4rem;
			background: #ffffff;

			// Position above month-header
			z-index: 10;

			padding-top: 20px;
			//margin-top: -30px;

			user-select: none;
		}

		.month-header {
			position: sticky;
			top: 60px;
			margin: 0;

			width: $date-aside-width;
			text-align: right;

			font-size: 1.2rem;
			background: #ffffff;

			// Position below year-header
			z-index: 9;

			padding-bottom: 15px;
			margin-bottom: -15px;
			//box-shadow: 0 30px 40px rgba(0,0,0,.1);

			user-select: none;
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
				user-select: none;

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
			// Bug is fixed now, reenabled. -2022-07-21
			position: sticky;
			top: 30px;
			width: 275px;
		}

		ol.datepicker {
			margin: 0;
			padding: 0;
			margin-bottom: 3rem;
			user-select: none;

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

		.filters-heading {
			user-select: none;
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
