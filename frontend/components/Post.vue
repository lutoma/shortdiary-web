<template>
	<el-card class="post" v-if="post">
		<div slot="header" class="post-header clearfix">
			<n-link v-if="showDate" :to="`/posts/${post.id}`" class="date">{{ date.toLocaleString('en', { month: "long" }) }} {{ date.getDate() }}, {{ date.getFullYear() }}</n-link>

			<template v-if="!compact && showDate">
				<el-divider direction="vertical" />
				{{ date.toLocaleString('en',  { weekday: 'long' }) }}
			</template>

			<template v-if="!compact">
				<el-divider direction="vertical" />
				<template v-if="post.public"><fa :icon="['fal', 'lock-open']" /> Public</template>
				<template v-else><fa :icon="['fal', 'lock']" /> Private</template>
			</template>

			<template v-if="post.location_verbose">
				<el-divider direction="vertical" />
				<fa :icon="['fal', 'map-marked-alt']" /> {{ post.location_verbose }}
			</template>

			<template v-if="post.mood">
				<el-divider direction="vertical" />
				<MoodIndicatorIcon :mood="post.mood" /> Mood: {{ post.mood }}
			</template>

			<div class="right" v-if="post.is_own">
				<n-link :to="`/posts/${post.id}/edit`"><el-button class="edit-button" type="text"><fa :icon="['fal', 'pencil']" /> Edit</el-button></n-link>
				<el-button class="delete-button" type="text" @click="deletePost"><fa :icon="['fal', 'trash']" /> Delete</el-button>
			</div>
		</div>

		<component class="text" v-bind:is="PostTextComponent" />

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
import MoodIndicatorIcon from '~/components/MoodIndicatorIcon'
import CoolLightBox from 'vue-cool-lightbox'
import 'vue-cool-lightbox/dist/vue-cool-lightbox.min.css'

export default {
	components: {
		MoodIndicatorIcon,
		CoolLightBox
	},

	props: {
		post: { type: Object, default: {} },
		compact: { type: Boolean, default: false },
		showDate: { type: Boolean, default: true }
	},

	data() {
		return {
			lightboxIndex: null
		}
	},

	// Render post text using a dynamically generated component. This is needed
	// so we can use other Vue components, most notably <nuxt-link>, inside the
	// rendered markup, which would not be possible with v-html.
	computed: {
		PostTextComponent() {
			let text_html = this.post.text || this.post.public_text
			text_html = text_html.replace(/(?:\r\n|\r|\n)/g, '<br>')
			text_html = text_html.replace(/@\w+\b/g, '<n-link to="/dashboard?filter=$&">$&</n-link>')

			return { template: `<div>${text_html}</div>` }
		},

		date() {
			return new Date(this.post.date)
		}
	},

	methods: {
		// FIXME needs to emit event for timeline reload/redirect from post detail page
		deletePost() {
			this.$confirm('This will permanently delete the post. Continue?', 'Warning', {
				confirmButtonText: 'OK',
				cancelButtonText: 'Cancel',
				type: 'warning'
			}).then(() => {
				this.$axios.$delete(`/posts/${this.post.id}`).then(() => {
					this.$emit('deleted')
					this.$message({
						type: 'success',
						message: 'Post deleted'
					})
				})
			})
		}
	}
}
</script>

<style lang="scss">
.post {
	.post-header {
		font-weight: 300;

		.date {
			font-weight: 400;
		}

		.el-rate {
			display: inline-block;
			margin-left: 2rem;
		}

		.right {
			float: right;
			padding: 3px 0;

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
