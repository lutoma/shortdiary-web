<template>
	<el-card class="post" v-if="post">
		<template #header>
			<ul>
				<li v-if="post.format_version === 0"><el-tag type="danger" effect="dark" style="font-weight: 400;"><fa :icon="['fal', 'lock-open']" /> Unencrypted</el-tag></li>
				<li v-if="showDate"><router-link :to="`/posts/${post.id}`" class="date">{{ date.toLocaleString('en', { month: "long" }) }} {{ date.getDate() }}, {{ date.getFullYear() }}</router-link></li>
				<li v-if="!compact && showDate">{{ date.toLocaleString('en',  { weekday: 'long' }) }}</li>
				<li v-if="post.location_verbose"><fa :icon="['fal', 'map-marked-alt']" /> {{ post.location_verbose }}</li>
				<li v-if="post.mood"><MoodIndicatorIcon :mood="post.mood" /> Mood: {{ post.mood }}</li>
			</ul>

			<div class="right" v-if="editable">
				<router-link :to="{ name: 'edit-post', params: { id: post.id } }"><el-button class="edit-button" type="text"><fa :icon="['fal', 'pencil']" /> Edit</el-button></router-link>
				<el-popconfirm @confirm="do_delete" title="Are you sure you want to delete this entry?">
					<template #reference>
						<el-button class="delete-button" type="text"><fa :icon="['fal', 'trash']" /> Delete</el-button>
					</template>
				</el-popconfirm>
			</div>
		</template>

		<!--<component class="text" v-bind:is="PostTextComponent" />-->
		<div class="text">{{ post.text }}</div>

		<CoolLightBox
			v-if="this.post.images"
			:items="this.post.images.map(i => ({ src: i.image }))"
			:index="lightboxIndex"
			@close="lightboxIndex = null"
			:slideshow="false" />

		<el-image
			v-for="[index, image] of (post.images || []).entries()"
			:src="image.thumbnail || image.image"
			:key="image.id"
			@click="lightboxIndex = index"
			fit="cover" />

		<div class="tags" v-if="post.tags && post.tags.length">
			<el-tag
				v-for="tag of post.tags"
				:key="tag"
				size="medium"
				effect="dark"
				type="info">

				{{ tag }}
			</el-tag>
		</div>
	</el-card>
</template>

<script>
import MoodIndicatorIcon from '@/components/MoodIndicatorIcon.vue';
import CoolLightBox from 'vue-cool-lightbox';
import 'vue-cool-lightbox/dist/vue-cool-lightbox.min.css';
import { defineAsyncComponent } from 'vue';
import { usePosts } from '@/stores/posts';

const LocalComponent = defineAsyncComponent(
	() => new Promise((resolve) => {
		resolve({
			template: `
			<h2>
			This is a local component defined as async!
			</h2>
		`,
		});
	}),
);

export default {
	components: {
		MoodIndicatorIcon,
		CoolLightBox,
		LocalComponent,
	},

	props: {
		post: { type: Object, default: () => {} },
		compact: { type: Boolean, default: false },
		showDate: { type: Boolean, default: true },
		editable: { type: Boolean, default: true },
	},

	data() {
		return {
			lightboxIndex: null,
		};
	},

	// Render post text using a dynamically generated component. This is needed
	// so we can use other Vue components, most notably <nuxt-link>, inside the
	// rendered markup, which would not be possible with v-html.
	computed: {
		PostTextComponent() {
			let html = this.post.text || this.post.public_text;
			html = html.replace(/(?:\r\n|\r|\n)/g, '<br>');
			html = html.replace(/@\w+\b/g, '<router-link to="/dashboard?filter=$&">$&</router-link>');

			return { template: `<div>${html}</div>` };
		},

		date() {
			return new Date(this.post.date);
		},
	},

	methods: {
		do_delete() {
			const store = usePosts();
			store.delete_post(this.post.id);
		},
	},
};
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
