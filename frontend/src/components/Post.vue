<template>
	<el-card v-if="post" class="post">
		<template #header>
			<ul>
				<li v-if="post.format_version === 0">
					<el-tag type="danger" effect="dark" style="font-weight: 400;">
						<fa :icon="['fal', 'lock-open']" /> Unencrypted
					</el-tag>
				</li>
				<li v-if="showDate">
					<router-link :to="`/posts/${post.id}`" class="date">
						{{ date.toLocaleString('en', { month: "long" }) }} {{ date.getDate() }}, {{ date.getFullYear() }}
					</router-link>
				</li>
				<li v-if="!compact && showDate">
					{{ date.toLocaleString('en', { weekday: 'long' }) }}
				</li>
				<li v-if="post.location_verbose">
					<fa :icon="['fal', 'map-marked-alt']" /> {{ post.location_verbose }}
				</li>
				<li v-if="post.mood">
					<MoodIndicatorIcon :mood="post.mood" /> Mood: {{ post.mood }}
				</li>
			</ul>

			<div v-if="editable" class="right">
				<router-link :to="{ name: 'edit-post', params: { id: post.id } }">
					<el-button class="edit-button" type="text">
						<fa :icon="['fal', 'pencil']" /> Edit
					</el-button>
				</router-link>
				<el-popconfirm title="Are you sure you want to delete this entry?" @confirm="doDelete">
					<template #reference>
						<el-button class="delete-button" type="text">
							<fa :icon="['fal', 'trash']" /> Delete
						</el-button>
					</template>
				</el-popconfirm>
			</div>
		</template>

		<PostTextComponent class="text" :text="post.text" />

		<CoolLightBox
			v-if="post.images"
			:items="post.images.map(i => ({ src: i.image }))"
			:index="lightboxIndex"
			:slideshow="false"
			@close="lightboxIndex = null"
		/>

		<el-image
			v-for="[index, image] of (post.images || []).entries()"
			:key="image.id"
			:src="image.thumbnail || image.image"
			fit="cover"
			@click="lightboxIndex = index"
		/>

		<div v-if="post.tags && post.tags.length" class="tags">
			<el-tag
				v-for="tag of post.tags"
				:key="tag"
				size="medium"
				effect="dark"
				type="info"
			>
				{{ tag }}
			</el-tag>
		</div>
	</el-card>
</template>

<script setup>
import MoodIndicatorIcon from '@/components/MoodIndicatorIcon.vue';
import CoolLightBox from 'vue-cool-lightbox';
import 'vue-cool-lightbox/dist/vue-cool-lightbox.min.css';
import { usePosts } from '@/stores/posts';
import { reactive, computed, h } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
	post: { type: Object, default: () => {} },
	compact: { type: Boolean, default: false },
	showDate: { type: Boolean, default: true },
	editable: { type: Boolean, default: true },
});

const lightboxIndex = reactive(null);
const date = computed(() => new Date(props.post.date));

function PostTextComponent() {
	// Split string along mentions and newlines
	let split = props.post.text.split(/(@\w+|\r?\n)/g);

	// Now replace mentions and newlines with html elements/router-link components
	split = split.map((x) => {
		if (x[0] === '@') {
			return h(RouterLink, { to: { name: 'timeline', query: { filter: x } } }, x);
		}

		if (x === '\n') {
			return h('br');
		}

		return x;
	});

	return h('div', split);
}

function doDelete() {
	const store = usePosts();
	store.delete_post(props.post.id);
}
</script>

<style lang="scss">
.post {
	.el-card__header {
		font-weight: 300;
		display: flex;
		flex-direction: row;
		align-items: center;

		ul {
			list-style-type: none;
			margin: 0;
			padding: 0;
			flex-grow: 1;

			li {
				display: inline-block;

				&:not(:first-of-type) {
					border-left: 1px solid #DCDFE6;
					margin-left: 8px;
					padding-left: 14px;

				}
			}

			.date {
				font-weight: 400;
			}

			.el-rate {
				display: inline-block;
				margin-left: 2rem;
			}
		}

		.right {
			.el-button {
				padding: 0;
				margin-left: .5rem;
			}
		}
	}

	.text {
		line-height: 1.5;
		font-size: 1.05rem;
	}

	.tags {
		margin-top: 1rem;

		.el-tag {
			margin-right: .3rem;
		}
	}

	.el-image {
		width: 125px;
		height: 125px;

		margin-top: 2rem;
		margin-right: .5rem;

		cursor: pointer;
		border: 1px solid #c0ccda;
		background-color: #fff;
		padding: 3px;
		transition: filter .3s;

		&:hover {
			filter: brightness(70%);
		}

		&, img {
			border-radius: 6px;
		}
	}
}
</style>
