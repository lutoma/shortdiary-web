import { defineStore } from 'pinia';
import api from '@/api';
import { encrypt, decrypt } from '@/crypto';
import sodium from 'libsodium-wrappers';
import { ElNotification } from 'element-plus';
import { useAuth } from './auth';

import flow from 'lodash/fp/flow';
import countBy from 'lodash/fp/countBy';
import toPairs from 'lodash/fp/toPairs';
import sortBy from 'lodash/fp/sortBy';
import reverse from 'lodash/fp/reverse';
import filter from 'lodash/fp/filter';
import map from 'lodash/fp/map';
import flatten from 'lodash/fp/flatten';

export const usePosts = defineStore('post', {
	state: () => {
		return {
			loaded: false,
			posts: new Map(),
			legacyPosts: [],
			mentions: [],
			locations: [],
			tags: [],
		};
	},

	getters: {
		postsList: (state) => [...state.posts.values()],

		mentions: (state) => {
			// Extract top mentions for use in stats.vue and PostEditor component
			const mentions = [];
			for (const [_, post] of state.posts) {
				// FIXME Should deduplicate/DRYfy regex with Post.vue
				// Temporarily cast to Set to deduplicate mentions within a post
				mentions.push(...[...new Set(post.text.toLowerCase().match(/@\w+\b/g))]);
			}

			return flow([
				countBy((x) => x),
				toPairs,
				sortBy(1),
				reverse,
			])(mentions);
		},

		locations: (state) => {
			return flow(
				filter('location_verbose'),
				countBy('location_verbose'),
				toPairs,
				sortBy(1),
				reverse,
			)(state.postsList);
		},

		tags: (state) => {
			return flow([
				map('tags'),
				flatten,
				countBy((x) => x),
				toPairs,
				sortBy(1),
				reverse,
			])(state.postsList);
		},
	},

	actions: {
		/* eslint-disable no-unused-vars */
		async load(force = false) {
			const authStore = useAuth();
			if (!authStore.masterKey) {
				return;
			}

			const res = await api.get('/posts');
			const posts = new Map();
			const legacyPosts = [];

			for await (const cpost of res.data) {
				let postData = null;

				switch (cpost.format_version) {
				case 0:
					// Unencrypted legacy posts
					postData = cpost.data;
					legacyPosts.push(cpost.id);
					break;
				case 1:
					try {
						postData = sodium.to_string(await decrypt(authStore.masterKey, cpost.nonce, cpost.data));
					} catch (err) {
						console.error(`Could not decrypt post ${cpost.id}: ${err.toString()}`);
						ElNotification({
							title: 'Decryption error',
							message: `Could not decrypt post ${cpost.id}: ${err.toString()}`,
						});
						continue;
					}
					break;
				default:
					console.error('Unknown post format version', cpost.format_version);
					continue;
				}

				const data = JSON.parse(postData);
				data.id = cpost.id;
				data.format_version = cpost.format_version;

				// FIXME
				data.images = null;
				posts.set(data.id, data);
			}

			this.posts = posts;
			this.legacyPosts = legacyPosts;
			this.loaded = true;
		},

		async delete_post(id) {
			await api.delete(`/posts/${id}`);
			ElNotification({
				title: 'Post deleted',
				message: 'The post has successfully been deleted.',
			});

			this.posts.delete(id);
		},

		async store_post(post, notify = true) {
			const jsonData = JSON.stringify(post);
			const authStore = useAuth();
			const [nonce, data] = await encrypt(authStore.masterKey, sodium.from_string(jsonData));

			const envelope = {
				nonce,
				data,
				date: post.date,
				format_version: 1,
			};

			if (post.id) {
				await api.put(`/posts/${post.id}`, envelope);
			} else {
				await api.post('/posts', envelope);
			}

			this.posts.set(post.id, post);

			if (notify) {
				ElNotification({
					title: 'Entry saved',
					message: post.id ? 'The changes to your entry have been saved.' : 'Your entry has been saved.',
				});
			}
		},
	},
});
