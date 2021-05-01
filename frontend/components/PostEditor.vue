<template>
	<el-row :gutter="50" class="post-editor">
		<el-col :span="19" class="main-area">
			<Mentionable :keys="['@']" :items="items" offset="6" insert-space>

				<el-input
					ref="text"
					type="textarea"
					:autosize="{ minRows: 15 }"
					placeholder="Jot down your adventures here"
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
						<el-option label="Yesterday" value="2021-04-26"/>
						<el-option label="Today" value="2021-04-27" />
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

				<div class="post-map-container" v-loading="!this.post.location">
					<Map
						v-if="this.post.location"
						:zoom="11"
						:center="this.post.location"
						:controls="false"
						:markers="this.post.location ? [this.post.location] : []"
						style="height: 100%" />
				</div>

				<el-form-item>
					<el-button type="primary" :disabled="!this.post.text.length" @click="savePost">
						<template v-if="!post.public">Save private entry</template>
						<template v-if="post.public">Save public entry</template>
					</el-button>
				</el-form-item>
			</el-form>
		</el-col>
	</el-row>
</template>

<script>
import { Mentionable } from 'vue-mention'
import { keyBy } from 'lodash'
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
				date: '2021-04-26',
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

		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(this.geoLocationCallback)
		}
	},

	methods: {
		updateLengthCounter() {
			// FIXME Should probably be a computed property
			this.text_length = {
				chars: this.post.text.length,
				words: this.post.text.split(' ').length - 1,
				sentences: this.post.text.split(/[.?!:;…‽⸮"«“]+/).length - 1
			}
		},

		geoLocationCallback(position) {
			this.post.location = [position.coords.longitude, position.coords.latitude]

			const url = `/map/geocoding/v5/mapbox.places/${position.coords.longitude}%2C%20${position.coords.latitude}.json?access_token=pk.eyJ1IjoibHV0b21hIiwiYSI6ImxEWUZyYTAifQ.pTzQYyVqJUgcojuuIDchbQ`

			this.$axios({ url, baseURL: '' }).then(({ data }) => {
				if (!data || !data.features) {
					return
				}

				const feat = keyBy(data.features, 'place_type.0')

				if ('place' in feat) {
					this.location_name = `${feat.place.text}, ${feat.country.text}`
				} else if ('region' in feat) {
					this.location_name = `${feat.region.text}, ${feat.country.text}`
				} else if ('country' in feat) {
					this.location_name = feat.country.text
				}
			})
		},

		async savePost() {
			if (!this.post.text.length) {
				return
			}

			// FIXME error handling
			await this.$axios.$post('/posts/', this.post)

			this.$router.push('/dashboard', () => {
				this.$message({ type: 'success', message: 'Your post has been added.' })
			})
		}
	}
}
</script>

<style lang="scss">
.post-editor {
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

	.post-map-container {
		height: 200px;
	}
}
</style>
