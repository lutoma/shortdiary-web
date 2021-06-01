<template>
	<div class="post-editor">
		<div class="editor-grid">
			<div class="main-area">
				<Mentionable
					:keys="['@']"
					:items="mention_items"
					placement="bottom-end"
					offset="6"
					insert-space>

					<el-input
						ref="text"
						type="textarea"
						:autosize="{ minRows: 15 }"
						placeholder="Jot down your adventures here"
						v-model="post.text"
						autofocus />
				</Mentionable>

				<el-button type="primary" :disabled="!this.post.text.length" @click="savePost">
					<template v-if="post.public">Save public entry</template>
					<template v-else>Save private entry</template>
				</el-button>
			</div>

			<div class="sidebar">
				<el-card>
					<el-form ref="form" :model="post" label-position="left" label-width="100px" @submit="savePost">
						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'calendar-alt']" /> Date
							</template>
							<el-date-picker
								v-model="post.date"
								type="date"
								placeholder="Pick a date"
								:picker-options="datePickerOptions"
								format="MMMM dd, yyyy"
								value-format="yyyy-MM-dd" />
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'shield-check']" /> Visibility
							</template>
							<el-radio-group v-model="post.public" size="small">
								<el-radio-button :label="true"><fa :icon="['far', 'lock-open']" /> Public</el-radio-button>
								<el-radio-button :label="false"><fa :icon="['far', 'lock']" /> Private</el-radio-button>
							</el-radio-group>
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<MoodIndicatorIcon :mood="post.mood === null ? 10 : post.mood" /> Mood
							</template>
							<el-slider v-model="post.mood" :step="1" :min="1" :max="10" show-stops />
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'map-marked-alt']" /> Location
							</template>
							<span v-loading="!post.location_verbose">{{ post.location_verbose }}</span>
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'images']" /> Images
							</template>
							<el-upload
								ref="images"
								:http-request="uploadImage"
								list-type="picture-card"
								:thumbnail-mode="true"
								:auto-upload="false"
								multiple>

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
import MoodIndicatorIcon from '~/components/MoodIndicatorIcon'

export default {
	components: {
		Mentionable,
		MapBackground,
		MoodIndicatorIcon
	},

	async fetch() {
		await this.$store.dispatch('updatePosts')
	},

	computed: {
		mention_items() {
			const mentions = this.$store.state.top_mentions.map(
				([mention, _]) => mention.substring(1))
			return mentions.map(value => ({ value, label: value }))
		}
	},

	data() {
		return {
			datePickerOptions: {
				firstDayOfWeek: 1,
				disabledDate(time) {
					return time.getTime() > Date.now()
				}
			},

			post: {
				id: null,
				public: false,
				text: '',

				// Super hacky and not timezone-aware
				date: new Date().toISOString().slice(0, 10),
				mood: 6,
				location: null,
				location_verbose: ''
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
		geoLocationCallback(position) {
			this.post.location = [position.coords.longitude, position.coords.latitude]

			const url = `/map/geocoding/v5/mapbox.places/${position.coords.longitude}%2C%20${position.coords.latitude}.json?access_token=pk.eyJ1IjoibHV0b21hIiwiYSI6ImxEWUZyYTAifQ.pTzQYyVqJUgcojuuIDchbQ`

			this.$axios({ url, baseURL: '' }).then(({ data }) => {
				if (!data || !data.features) {
					return
				}

				const feat = keyBy(data.features, 'place_type.0')

				if ('place' in feat) {
					this.post.location_verbose = `${feat.place.text}, ${feat.country.text}`
				} else if ('region' in feat) {
					this.post.location_verbose = `${feat.region.text}, ${feat.country.text}`
				} else if ('country' in feat) {
					this.post.location_verbose = feat.country.text
				}
			})
		},

		async savePost() {
			if (!this.post.text.length) {
				return
			}

			// FIXME Better error handling
			this.post = await this.$axios.$post('/posts/', this.post)
			await this.$refs.images.submit()

			this.$store.dispatch('updatePosts')
			this.$router.push('/dashboard', () => {
				this.$message({ type: 'success', message: 'The entry has been added.' })
			})
		},

		uploadImage(req) {
			const data = new FormData()
			data.append('post', this.post.id)
			data.append('image', req.file)

			const config = {
				headers: { 'Content-Type': 'multipart/form-data' },
				onUploadProgress: ev => {
					req.onProgress({ percent: Math.floor((ev.loaded * 100) / ev.total) })
				}
			}

			this.$axios.$post('/post_images/', data, config).then(res => req.onSuccess(res))
		}
	}
}
</script>

<style lang="scss">
.post-editor {
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

// FIXME Need to properly scope this to not affect other potential popvers?
.tooltip.popover {
	background: white;
	box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
	border-radius: 4px;
	overflow: hidden;

	.tooltip-inner {
		min-width: 80px;
		color: #606266;
		font-size: 14px;

		div > * {
			padding: 4px 8px;
		}

		.mention-selected {
			background: #CDB380;
			color: white;
		}
	}
}
</style>
