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

				<el-button type="primary" :disabled="!pdata.text" v-model:loading="loading" @click="save">
					Save entry
				</el-button>
			</div>

			<div class="sidebar">
				<el-card>
					<el-form ref="form" :model="pdata" label-position="left" label-width="100px" @submit="save">
						<el-form-item>
							<template #label>
								<fa :icon="['fal', 'calendar-alt']" /> Date
							</template>
							<el-date-picker
								v-model="pdata.date"
								type="date"
								placeholder="Pick a date"
								:picker-options="datePickerOptions"
								format="MMMM DD, YYYY"
								value-format="YYYY-MM-DD" />
						</el-form-item>

						<el-form-item>
							<template #label>
								<MoodIndicatorIcon :mood="pdata.mood === null ? 10 : pdata.mood" /> Mood
							</template>
							<el-slider v-model="pdata.mood" :step="1" :min="1" :max="10" show-stops />
						</el-form-item>

						<el-form-item>
							<template #label>
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
							<template #label>
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
							<template #label>
								<fa :icon="['fal', 'images']" /> Images
							</template>
							<el-upload
								ref="images"
								v-model:file-list="existing_images"
								action="#"
								list-type="picture-card"
								:on-preview="handlePictureCardPreview"
								:on-remove="removeImage"
								:auto-upload="false"
								:http-request="uploadImage"
								>

								<el-icon><Plus /></el-icon>
							</el-upload>

							<el-dialog v-model="dialogVisible">
								<img w-full :src="dialogImageUrl" alt="Preview Image" />
							</el-dialog>

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
import { mapState } from 'pinia';
import { usePosts } from '@/stores/posts';

import api from '@/api';
import { Mentionable } from 'vue-mention';
import { cloneDeep } from 'lodash';
import { get_error } from '@/utils';
import { ElNotification } from 'element-plus';

import MapBackground from '@/components/MapBackground.vue';
import MoodIndicatorIcon from '@/components/MoodIndicatorIcon.vue';

// Default data for newly created posts
const default_pdata = {
	text: '',

	// Super hacky and not timezone-aware
	date: new Date().toISOString().slice(0, 10),
	mood: 6,
	tags: [],
	location_lat: null,
	location_lon: null,
	location_verbose: '',
};

export default {
	components: {
		Mentionable,
		MapBackground,
		MoodIndicatorIcon,
	},

	props: {
		post: { type: Object, default: null },
	},

	data() {
		return {
			datePickerOptions: {
				firstDayOfWeek: 1,
				disabledDate(time) {
					return time.getTime() > Date.now();
				},
			},

			// true if the save operation is loading
			loading: false,

			// Errors returned from API
			error: {},

			// Main post data object. This is what will be sent to the server
			// in the API request. Filled with either the post we want to edit
			// (passed in through the prop), or the default post template
			pdata: this.post || cloneDeep(default_pdata),

			// When editing a post, IDs of images to delete upon save
			images_to_delete: [],
		};
	},

	computed: {
		...mapState(usePosts, ['top_mentions', 'top_tags']),

		mention_items() {
			const mentions = this.top_mentions.map(
				([mention, _]) => mention.substring(1),
			);
			return mentions.map((value) => ({ value, label: value }));
		},

		existing_images() {
			if (!this.post || !this.post.images) {
				return [];
			}

			return this.post.images.map((x) => ({ id: x.id, url: x.thumbnail }));
		},
	},

	methods: {
		get_error,

		geoLocationCallback(position) {
			this.pdata.location_lat = String(position.coords.latitude).substr(0, 14);
			this.pdata.location_lon = String(position.coords.longitude).substr(0, 14);

			const url = `/geocode/v1/json?q=${this.pdata.location_lat}%2C%20${this.pdata.location_lon}&language=en&no_annotations=1&no_record=1&key=849a36fca0e949fc91000924584ac0c4`;

			api({ url, baseURL: '' }).then(({ data }) => {
				if (!data || data.total_results < 1) {
					return;
				}

				if (!('components' in data.results[0])) {
					return;
				}

				const res = data.results[0].components;
				if ('city' in res) {
					this.pdata.location_verbose = `${res.city}, ${res.country}`;
				} else if ('town' in res) {
					this.pdata.location_verbose = `${res.town}, ${res.country}`;
				} else if ('county' in res) {
					this.pdata.location_verbose = `${res.county}, ${res.country}`;
				} else if ('state' in res) {
					this.pdata.location_verbose = `${res.state}, ${res.country}`;
				} else if ('country' in res) {
					this.pdata.location_verbose = res.country;
				}
			});
		},

		getGeoLocation() {
			// FIXME Display some nice message if geolocation fails
			if (navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(this.geoLocationCallback);
			}
		},

		async save() {
			if (!this.pdata.text.length) {
				return;
			}

			this.error = {};
			this.loading = true;

			// Delete removed images for existing posts
			for (const id of this.images_to_delete) {
				await api.$delete(`/post_images/${id}/`);
			}

			const store = usePosts();
			await store.store_post(this.pdata);

			// Upload new images
			await this.$refs.images.submit();

			this.loading = false;
			this.$router.push({ name: 'timeline' });
		},

		uploadImage(req) {
			const data = new FormData();
			data.append('post', this.post.id);
			data.append('image', req.file);

			const config = {
				headers: { 'Content-Type': 'multipart/form-data' },
				onUploadProgress: (ev) => {
					req.onProgress({ percent: Math.floor((ev.loaded * 100) / ev.total) });
				},
			};

			api.post('/post_images/', data, config).then((res) => req.onSuccess(res));
		},

		removeImage(file, _) {
			// If we're editing a post and this image has already been
			// uploaded, mark it for deletion on save.
			if ('id' in file) {
				this.images_to_delete.push(file.id);
			}
		},
	},

	mounted() {
		this.$refs.text.$el.children[0].focus();

		if (!(this.post && this.post.id)) {
			this.getGeoLocation();
		}
	},
};
</script>

<style lang="scss">
.post-editor {
	height: 100%;
	display: flex;
	flex-direction: column;

	> .el-alert {
		margin-bottom: 1rem;
	}

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
