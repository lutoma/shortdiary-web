<template>
	<el-card class="post" v-if="post">
		<div slot="header" class="clearfix">
			<el-tag size="small" :type="post.public ? 'default' : 'warning'">
				<template v-if="post.public"><fa :icon="['far', 'lock-open']" /> Public</template>
				<template v-if="!post.public"><fa :icon="['far', 'lock']" /> Private</template>
			</el-tag>
			<span>{{ post.date }} <template v-if="post.location_verbose">| {{ post.location_verbose }}</template></span>

			<el-rate v-model="post.mood" disabled />
			<el-button v-if="post.is_editable" class="edit-button" type="text"><fa :icon="['far', 'pencil']" /> Edit</el-button>
		</div>

		<div class="text" v-html="text_html" />

		<CoolLightBox :items="[{src: this.post.image}]" :index="lightboxIndex" @close="lightboxIndex = null" :slideshow="false" />
		<el-image v-if="post.image" :src="post.image" :fit="fit" @click="lightboxIndex = 0" />
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
	},

	data() {
		let text = this.post.text || this.post.public_text

		return {
			text_html: text.replace(/(?:\r\n|\r|\n)/g, '<br>'),
			lightboxIndex: null,

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

	.edit-button {
		float: right;
		padding: 3px 0;
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
