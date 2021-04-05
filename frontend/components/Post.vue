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
				<n-link v-if="showPermalink" :to="`/posts/${post.id}`"><el-button type="text"><fa :icon="['far', 'link']" /> Permalink</el-button></n-link>
			</div>
		</div>

		<div class="text" v-html="text_html" />

		<CoolLightBox :items="[{src: this.post.image}]" :index="lightboxIndex" @close="lightboxIndex = null" :slideshow="false" />
		<el-image v-if="post.image" :src="post.image" fit="fit" @click="lightboxIndex = 0" />
	</el-card>
</template>

<script>
//import marked from 'marked'
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
		const text = this.post.text || this.post.public_text

		return {
			text_html: text.replace(/(?:\r\n|\r|\n)/g, '<br>'),
			lightboxIndex: null

			// Rendering as markdown unfortunately breaks old posts
			// text_html: marked(this.post.text)
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
