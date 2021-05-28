<template>
	<div class="post-editor">
		<div class="editor-grid">
			<div class="main-area">
				<Mentionable :keys="['@']" :items="items" offset="6" insert-space>

					<el-input
						ref="text"
						type="textarea"
						:autosize="{ minRows: 15 }"
						placeholder="Jot down your adventures here"
						v-model="post.text"
						autofocus />
				</Mentionable>

				<el-button type="primary" :disabled="!this.post.text.length" @click="savePost">
					<template v-if="!post.public">Save private entry</template>
					<template v-if="post.public">Save public entry</template>
				</el-button>
			</div>

			<div class="sidebar">
				<el-card>
					<el-form ref="form" :model="post" label-position="left" label-width="100px" @submit="savePost">
						<el-form-item label="Date">
							<el-select v-model="post.date" placeholder="Date">
								<el-option v-for="option of dateOptions" :label="option.label" :value="option.date"/>
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
						<el-form-item label="Images">
							<el-upload
								action="https://jsonplaceholder.typicode.com/posts/"
								list-type="picture-card"
								:thumbnail-mode="true"
								:auto-upload="false">

								<i class="el-icon-plus"></i>
							</el-upload>
						</el-form-item>
					</el-form>
				</el-card>
			</div>
		</div>
		<MapBackground v-if="post.location" :center="post.location" />
	</div>
</template>

<script>
import { Mentionable } from 'vue-mention'
import { keyBy } from 'lodash'
import MapBackground from '~/components/MapBackground'

export default {
	components: {
		Mentionable,
		MapBackground
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

			location_name: null
		}
	},

	computed: {
		dateOptions() {
			const today = new Date()
			const yesterday = today
			yesterday.setDate(yesterday.getDate() - 1)

			return [
				{ label: 'Yesterday', date: yesterday.toISOString().slice(0, 10) },
				{ label: 'Today', date: today.toISOString().slice(0, 10) }
			]
		}
	},

	mounted() {
		this.$refs.text.$el.children[0].focus()

		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(this.geoLocationCallback)
		}
	},

	methods: {
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
	padding-bottom: 30px;

	height: 100%;
	display: flex;
	flex-direction: column;

	.editor-grid {
		width: 100%;
		flex-grow: 1;
		display: flex;

	}
	.main-area, .mentionable {
		height: 100%;
		flex: 1 1 100%;
		display: flex;
		flex-direction: column;
	}

	.main-area {
		margin-right: 30px;

		.el-button {
			width: 250px;
			max-width: 100%;
			margin-top: 15px;
			align-self: flex-end;
		}

		.el-textarea {
			flex-grow: 1;

			.el-textarea__inner {
				height: 100% !important;
				font-size: 1rem;
			}
		}
	}

	.sidebar {
		flex: 0.1 0 350px;

		.el-upload--picture-card, .el-upload-list--picture-card .el-upload-list__item {
			width: 72px;
			height: 72px;
		}

		.el-upload--picture-card {
			line-height: initial;
			display: inline-flex;
			justify-content: center;
			align-items: center;
		}
	}
}
</style>
