<template>
	<div class="new-post">
		<h1>New entry</h1>
		<el-row :gutter="50">
			<el-col :span="19" class="main-area">
				<Mentionable :keys="['@']" :items="items" offset="6" insert-space>

					<el-input
						ref="text"
						type="textarea"
						:autosize="{ minRows: 15 }"
						:placeholder="`Jot down ${this.post.date}'s adventures here`"
						v-model="post.text"
						autofocus
						@input="updateLengthCounter()" />
				</Mentionable>

				<div class="length-counter">
					<template v-if="text_length.chars > 800">Wow, what an eventful day!</template>
					{{ text_length.sentences}} sentences, {{ text_length.words }} words, {{ text_length.chars }} characters
				</div>

				<h2>Images</h2>
				<el-upload
					action="https://jsonplaceholder.typicode.com/posts/"
					list-type="picture-card"
					:thumbnail-mode="true"
					:auto-upload="false">

					<i class="el-icon-plus"></i>
				</el-upload>
			</el-col>

			<el-col :span="5" class="index-sidebar">
				<el-form ref="form" :model="post" label-position="top" label-width="60px" @submit="savePost">
					<el-form-item label="Date">
						<el-select v-model="post.date" placeholder="Date">
							<el-option label="Yesterday" value="yesterday"/>
							<el-option label="Today" value="today" />
						</el-select>
					</el-form-item>

					<el-form-item label="Visibility">
						<el-radio-group v-model="post.visibility" size="small">
							<el-radio-button label="public"><fa :icon="['far', 'lock-open']" /> Public</el-radio-button>
							<el-radio-button label="private"><fa :icon="['far', 'lock']" /> Private</el-radio-button>
						</el-radio-group>
					</el-form-item>

					<el-form-item label="Mood">
						<el-slider v-model="post.mood" :step="1" :min="1" :max="10" show-stops />
					</el-form-item>

					<el-form-item label="Location">
						<span v-loading="!this.location_name">{{ this.location_name }}</span>
					</el-form-item>

<!--
					<Map
						v-loading="this.post.location"
						:zoom="11"
						:center="this.post.location"
						:options="{zoomControl: false}"
						:markers="this.post.location ? [this.post.location] : []" />
-->

					<el-form-item>
						<el-button type="primary" :disabled="!this.post.text.length" @click="savePost">
							<template v-if="!post.public">Save private entry</template>
							<template v-if="post.public">Save public entry</template>
						</el-button>
					</el-form-item>
				</el-form>
			</el-col>
		</el-row>
	</div>
</template>

<script>
import { Mentionable } from 'vue-mention'
import Map from '~/components/Map'

export default {
	components: {
		Mentionable,
		Map
	},
	data() {
		return {
			post: {
				visibility: 'private',
				text: '',
				date: 'yesterday',
				mood: null,
				location: null
			},

			location_name: null,

			text_length: {
				sentences: 0,
				words: 0,
				chars: 0
			}
		}
	},

	mounted() {
		this.$refs.text.$el.children[0].focus()

		if(navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(this.geoLocationCallback);
		}
	},

	methods: {
		updateLengthCounter() {
			// FIXME Should probably be a computed property
			this.text_length = {
				chars: this.post.text.length,
				words: this.post.text.split(' ').length - 1,
				sentences: this.post.text.split(/[\.\?\!:;…‽⸮"«“]+/).length - 1
			}
		},

		geoLocationCallback(position) {
			this.post.location = [position.coords.latitude, position.coords.longitude]
			const url = `/maptiler/geocoding/${position.coords.longitude},${position.coords.latitude}.json`

			this.$axios({ url, baseURL: '' }).then(({ data }) => {
				if (!data || !data.features) {
					return
				}

				// We don't want to go all the way down to street/subcity level
				const features = data.features.filter(feature => !['street', 'subcity'].includes(feature.place_type[0]))

				// Now pick the most exact name the API has to offer (Usually 'city', sometimes 'county' or even 'country' if nothing better is available)
				if (features) {
					this.location_name = features[0].text
				}
			})
		},

		async savePost() {
			if (!this.post.text.length) {
				return
			}

			//const req = await this.$axios.$put('/posts/')
			//console.log(req)

			this.$router.push('/dashboard', () => {
				this.$message({ type: 'success', message: 'Your post has been added.' });
			})
		}
	}
};
</script>

<style lang="scss">
.new-post {
	height: 100%;
	display: flex;
	flex-direction: column;

	.el-row {
		width: 100%;
		flex-grow: 1;
	}

	.main-area, .mentionable {
		height: 100%;
		display: flex;
		flex-direction: column;

	}

	.el-textarea {
		flex-grow: 1;

		.el-textarea__inner {
			height: 100% !important;
			font-size: 1.05rem;
		}
	}

	.length-counter {
		font-size: 14px;
		color: #606266;
		text-align: right;
		margin-top: .5rem;
	}

	.el-button {
		margin-top: .5rem;
	}
}
</style>
