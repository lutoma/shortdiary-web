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
						placeholder="Jot down your adventures here"
						v-model="pdata.text"
						autofocus />
				</Mentionable>

				<el-button type="primary" :disabled="!this.pdata.text" @click="save">
					<template v-if="pdata.public">Save public entry</template>
					<template v-else>Save private entry</template>
				</el-button>
			</div>

			<div class="sidebar">
				<el-card>
					<el-form ref="form" :model="pdata" label-position="left" label-width="100px" @submit="save">
						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'calendar-alt']" /> Date
							</template>
							<el-date-picker
								v-model="pdata.date"
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
							<el-radio-group v-model="pdata.public" size="small">
								<el-radio-button :label="true"><fa :icon="['far', 'lock-open']" /> Public</el-radio-button>
								<el-radio-button :label="false"><fa :icon="['far', 'lock']" /> Private</el-radio-button>
							</el-radio-group>
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<MoodIndicatorIcon :mood="pdata.mood === null ? 10 : pdata.mood" /> Mood
							</template>
							<el-slider v-model="pdata.mood" :step="1" :min="1" :max="10" show-stops />
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'tags']" /> Tags
							</template>
							<el-select
								v-model="pdata.tags"
								multiple
								filterable
								allow-create
								default-first-option
								placeholder="Choose tags">

								<el-option
									v-for="item in top_tags"
									:key="item[0]"
									:label="item[0]"
									:value="item[0]" />
							</el-select>
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'map-marked-alt']" /> Location
							</template>
							<div v-loading="!pdata.location_verbose">
								{{ pdata.location_verbose }}

								<el-button type="text" v-if="post && post.id && pdata.location_verbose" @click="getGeoLocation()">
									<fa :icon="['far', 'sync']" />
								</el-button>
							</div>
						</el-form-item>

						<el-form-item>
							<template slot="label">
								<fa :icon="['fal', 'images']" /> Images
							</template>
							<el-upload
								ref="images"
								action="#"
								:http-request="uploadImage"
								:on-remove="removeImage"
								:file-list="existing_images"
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
		<MapBackground v-if="pdata.location_lat && pdata.location_lon" :center="[pdata.location_lon, pdata.location_lat]" />
	</div>
</template>

<script>
import { mapState } from 'vuex'
import { Mentionable } from 'vue-mention'
import { keyBy, cloneDeep } from 'lodash'
import MapBackground from '~/components/MapBackground'
import MoodIndicatorIcon from '~/components/MoodIndicatorIcon'

// Default data for newly created posts
const default_pdata = {
	public: false,
	text: '',

	// Super hacky and not timezone-aware
	date: new Date().toISOString().slice(0, 10),
	mood: 6,
	tags: [],
	location_lat: null,
	location_lon: null,
	location_verbose: ''
}

export default {
	components: {
		Mentionable,
		MapBackground,
		MoodIndicatorIcon
	},

	props: {
		post: { type: Object, default: null }
	},

	async fetch() {
		await this.$store.dispatch('updatePosts')
	},

	data() {
		return {
			datePickerOptions: {
				firstDayOfWeek: 1,
				disabledDate(time) {
					return time.getTime() > Date.now()
				}
			},

			// Main post data object. This is what will be sent to the server
			// in the API request. Filled with either the post we want to edit
			// (passed in through the prop), or the default post template
			pdata: this.post || cloneDeep(default_pdata),

			// When editing a post, IDs of images to delete upon save
			images_to_delete: []
		}
	},

	computed: {
		...mapState(['top_tags']),

		mention_items() {
			const mentions = this.$store.state.top_mentions.map(
				([mention, _]) => mention.substring(1))
			return mentions.map(value => ({ value, label: value }))
		},

		existing_images() {
			if (!this.post) {
				return []
			}

			return this.post.images.map(x => ({ id: x.id, url: x.thumbnail }))
		}
	},

	methods: {
		geoLocationCallback(position) {
			this.pdata.location_lat = position.coords.latitude
			this.pdata.location_lon = position.coords.longitude

			const url = `/map/geocoding/v5/mapbox.places/${position.coords.longitude}%2C%20${position.coords.latitude}.json?access_token=pk.eyJ1IjoibHV0b21hIiwiYSI6ImxEWUZyYTAifQ.pTzQYyVqJUgcojuuIDchbQ`

			this.$axios({ url, baseURL: '' }).then(({ data }) => {
				if (!data || !data.features) {
					return
				}

				const feat = keyBy(data.features, 'place_type.0')

				if ('place' in feat) {
					this.pdata.location_verbose = `${feat.place.text}, ${feat.country.text}`
				} else if ('region' in feat) {
					this.pdata.location_verbose = `${feat.region.text}, ${feat.country.text}`
				} else if ('country' in feat) {
					this.pdata.location_verbose = feat.country.text
				}
			})
		},

		getGeoLocation() {
			// FIXME Display some nice message if geolocation fails
			if (navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(this.geoLocationCallback)
			}
		},

		async save() {
			if (!this.pdata.text.length) {
				return
			}

			// Delete removed images for existing posts
			for (const id of this.images_to_delete) {
				await this.$axios.$delete(`/post_images/${id}/`)
			}

			// FIXME Better error handling
			if (this.post && this.post.id) {
				this.post = await this.$axios.$put(`/posts/${this.post.id}/`, this.pdata)
			} else {
				this.post = await this.$axios.$post('/posts/', this.pdata)
			}

			// Upload new images
			await this.$refs.images.submit()

			this.$router.push('/dashboard', () => {
				this.$message({ type: 'success', message: 'The entry has been saved' })
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
		},

		removeImage(file, list) {
			// If we're editing a post and this image has already been
			// uploaded, mark it for deletion on save.
			if ('id' in file) {
				this.images_to_delete.push(file.id)
			}
		}
	},

	mounted() {
		this.$refs.text.$el.children[0].focus()

		if (!(this.post && this.post.id)) {
			this.getGeoLocation()
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
