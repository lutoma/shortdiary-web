<template>
	<div class="post-editor">
		<div class="editor-grid">
			<div class="main-area">
				<Mentionable
					:keys="['@']"
					:items="mentionItems"
					placement="bottom-end"
					offset="6"
					insert-space
				>
					<el-input
						ref="textElement"
						v-model="pdata.text"
						type="textarea"
						placeholder="Jot down your adventures here. If you mention a person like this: @person, they will be listed in the 'People' tab."
						autofocus
					/>

					<template #no-result>
						<div class="mention-no-result">
							No result
						</div>
					</template>
				</Mentionable>
			</div>

			<div class="sidebar">
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
							value-format="YYYY-MM-DD"
						/>
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
							placeholder="Choose tags"
						>
							<el-option
								v-for="item in store.tags"
								:key="item[0]"
								:label="item[0]"
								:value="item[0]"
							/>
						</el-select>
					</el-form-item>

					<el-form-item>
						<template #label>
							<fa :icon="['fal', 'map-marked-alt']" /> Location
						</template>
						<div v-loading="!pdata.location_verbose">
							{{ pdata.location_verbose }}

							<el-button v-if="post && post.id && pdata.location_verbose" type="text" @click="getGeoLocation()">
								<fa :icon="['far', 'sync']" />
							</el-button>
						</div>
					</el-form-item>

					<el-form-item>
						<template #label>
							<fa :icon="['fal', 'images']" /> Images
						</template>
						<el-upload
							ref="imagesElement"
							v-model:file-list="existingImages"
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
							<img w-full :src="dialogImageUrl" alt="Preview Image">
						</el-dialog>

						<el-upload
							ref="imagesElement"
							action="#"
							:http-request="uploadImage"
							:on-remove="removeImage"
							:file-list="existingImages"
							list-type="picture-card"
							:thumbnail-mode="true"
							:auto-upload="false"
							multiple
						>
							<i class="el-icon-plus" />
						</el-upload>
					</el-form-item>
				</el-form>

				<el-button v-model:loading="loading" type="primary" :disabled="!pdata.text" @click="save">
					Save entry
				</el-button>
			</div>
		</div>
	</div>
</template>

<script setup>
import {
	ref, reactive, computed, onMounted,
} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { usePosts } from '@/stores/posts';
import api from '@/api';
import { Mentionable } from 'vue-mention';
import cloneDeep from 'lodash/cloneDeep';
import MoodIndicatorIcon from '@/components/MoodIndicatorIcon.vue';

// Default data for newly created posts
const defaultPdata = {
	text: '',

	// Super hacky and not timezone-aware
	date: new Date().toISOString().slice(0, 10),
	mood: 6,
	tags: [],
	location_lat: null,
	location_lon: null,
	location_verbose: '',
};

const datePickerOptions = {
	firstDayOfWeek: 1,
	disabledDate(time) {
		return time.getTime() > Date.now();
	},
};

const store = usePosts();
const router = useRouter();
const route = useRoute();

// Bit hacky, but eh
let editPost = null;
if (route.name === 'edit-post') {
	const postId = route.params.id;
	editPost = store.posts.get(postId);
}

const loading = ref(false);
const error = ref(null);

// Main post data object. Filled with either the post we want to edit
// (passed in through the prop), or the default post template
const pdata = reactive(editPost || cloneDeep(defaultPdata));

// When editing a post, IDs of images to delete upon save
const imagesToDelete = reactive([]);

const existingImages = computed(() => {
	if (!editPost || !editPost.images) {
		return [];
	}

	return editPost.images.map((x) => ({ id: x.id, url: x.thumbnail }));
});

const mentionItems = computed(() => {
	const mentions = store.mentions.map(
		([mention, _]) => mention.substring(1),
	);
	return mentions.map((value) => ({ value, label: value }));
});

function geoLocationCallback(position) {
	pdata.location_lat = String(position.coords.latitude).substr(0, 14);
	pdata.location_lon = String(position.coords.longitude).substr(0, 14);

	const url = `/geocode/v1/json?q=${pdata.location_lat}%2C%20${pdata.location_lon}&language=en&no_annotations=1&no_record=1&key=849a36fca0e949fc91000924584ac0c4`;

	api({ url, baseURL: '' }).then(({ data }) => {
		if (!data || data.total_results < 1) {
			return;
		}

		if (!('components' in data.results[0])) {
			return;
		}

		const res = data.results[0].components;
		if ('city' in res) {
			pdata.location_verbose = `${res.city}, ${res.country}`;
		} else if ('town' in res) {
			pdata.location_verbose = `${res.town}, ${res.country}`;
		} else if ('county' in res) {
			pdata.location_verbose = `${res.county}, ${res.country}`;
		} else if ('state' in res) {
			pdata.location_verbose = `${res.state}, ${res.country}`;
		} else if ('country' in res) {
			pdata.location_verbose = res.country;
		}
	});
}

function getGeoLocation() {
	// FIXME Display some nice message if geolocation fails
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(geoLocationCallback);
	}
}

const imagesElement = ref(null);
async function save() {
	if (!pdata.text.length) {
		return;
	}

	error.value = null;
	loading.value = true;

	// Delete removed images for existing posts
	for (const id of imagesToDelete) {
		await api.$delete(`/post_images/${id}/`);
	}

	await store.store_post(pdata);

	// Upload new images
	// await imagesElement.value.images.submit();

	loading.value = false;
	router.push({ name: 'timeline' });
}

function uploadImage(req) {
	const data = new FormData();
	data.append('post', editPost.id);
	data.append('image', req.file);

	const config = {
		headers: { 'Content-Type': 'multipart/form-data' },
		onUploadProgress: (ev) => {
			req.onProgress({ percent: Math.floor((ev.loaded * 100) / ev.total) });
		},
	};

	api.post('/post_images/', data, config).then((res) => req.onSuccess(res));
}

function removeImage(file, _) {
	// If we're editing a post and this image has already been
	// uploaded, mark it for deletion on save.
	if ('id' in file) {
		imagesToDelete.push(file.id);
	}
}

const textElement = ref(null);
onMounted(() => {
	textElement.value.$el.children[0].focus();

	if (!(editPost && editPost.id)) {
		getGeoLocation();
	}
});
</script>

<style lang="scss">
.post-editor {
	height: 70vh;
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
		flex: 0.1 0 300px;
		display: flex;
		flex-direction: column;

		.el-form {
			margin-bottom: 2rem;
//			flex-grow: 1;

			.el-form-item {
				.el-form-item__label {
					// Make sure font-awesome icons properly align vertically
					align-items: center;
				}

				.el-select, .el-input, .el-input__wrapper {
					width: 100%;
				}
			}

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
}

.v-popper__popper {
	// Rather hacky but for some reason the poppers end up to far left otherwise
	margin-left: 27px;

	.v-popper__wrapper {
		.mention-item, .mention-no-result {
			font-size: .85rem;
			padding: 4px 6px;
		}

		.mention-selected {
			background: var(--el-color-primary);
		}
	}
}
</style>
