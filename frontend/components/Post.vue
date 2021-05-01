<template>
	<el-card class="post" v-if="post">
		<div slot="header" class="clearfix">
			<el-tag size="small" :type="post.public ? 'default' : 'warning'">
				<template v-if="post.public"><fa :icon="['far', 'lock-open']" /> Public</template>
				<template v-if="!post.public"><fa :icon="['far', 'lock']" /> Private</template>
			</el-tag>
			<template v-if="showDate">{{ post.date }}</template> <template v-if="post.location_verbose">| {{ post.location_verbose }}</template>

			<el-rate v-model="post.mood" disabled />
			<div class="right">
				<el-button v-if="post.is_editable" class="edit-button" type="text"><fa :icon="['far', 'pencil']" /> Edit</el-button>
				<el-button v-if="post.is_editable" class="delete-button" type="text" @click="deletePost"><fa :icon="['far', 'trash']" /> Delete</el-button>
				<n-link v-if="showPermalink" :to="`/posts/${post.id}`"><el-button type="text"><fa :icon="['far', 'link']" /> Permalink</el-button></n-link>
			</div>
		</div>

		<component class="text" v-bind:is="PostTextComponent" />

		<CoolLightBox :items="[{src: this.post.image}]" :index="lightboxIndex" @close="lightboxIndex = null" :slideshow="false" />
		<el-image v-if="post.image" :src="post.image" fit="cover" @click="lightboxIndex = 0" />
	</el-card>
</template>

<script>
import CoolLightBox from 'vue-cool-lightbox'
import 'vue-cool-lightbox/dist/vue-cool-lightbox.min.css'

export default {
	components: {
		CoolLightBox
	},

	props: {
		post: { type: Object, default: {} },
		showDate: { type: Boolean, default: true },
		showPermalink: { type: Boolean, default: true }
	},

	data() {
		let text_html = this.post.text || this.post.public_text
		text_html = text_html.replace(/(?:\r\n|\r|\n)/g, '<br>')
		text_html = text_html.replace(/@\w+\b/g, '<n-link to="/dashboard?filter=$&">$&</n-link>')

		return {
			text_html,
			lightboxIndex: null
		}
	},

	// Render post text using a dynamically generated component. This is needed
	// so we can use other Vue components, most notably <nuxt-link>, inside the
	// rendered markup, which would not be possible with v-html.
	computed: {
		PostTextComponent() {
			return { template: `<div>${this.text_html}</div>` }
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

	.text {
		line-height: 1.3;
		font-size: 1.05rem;
		font-family: "Fira Sans";
	}

	.el-image {
		width: 125px;
		height: 125px;
		margin-top: 2rem;
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
