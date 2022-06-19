import { defineStore } from 'pinia';
import api from '@/api';
import _ from 'lodash';
import { encrypt, decrypt } from '@/crypto';
import sodium from 'libsodium-wrappers';
import { ElNotification } from 'element-plus';
import { useAuth } from './auth';

export const usePosts = defineStore('post', {
	state: () => {
		return {
			posts: new Map(),
			mentions: [],
			locations: [],
			tags: [],
		};
	},

	getters: {
		postsList: (state) => [...state.posts.values()],
	},

	actions: {
		async load() {
			const authStore = useAuth();
			if (!authStore.masterKey) {
				return;
			}

			const res = await api.get('/posts');
			const posts = new Map();
			for (const cpost of res.data) {
				let postData = null;

				switch (cpost.format_version) {
				case 0:
					// Unencrypted legacy posts
					postData = cpost.data;
					break;
				case 1:
					try {
						postData = sodium.to_string(decrypt(authStore.masterKey, cpost.nonce, cpost.data));
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

			// Extract top mentions for use in stats.vue and PostEditor component
			const mentions = [];
			for (const [_, post] of posts) {
				// FIXME Should deduplicate/DRYfy regex with Post.vue
				// Temporarily cast to Set to deduplicate mentions within a post
				mentions.push(...[...new Set(post.text.toLowerCase().match(/@\w+\b/g))]);
			}

			this.mentions = _(mentions)
				.countBy()
				.toPairs()
				.sortBy(1)
				.reverse()
				.value();

			const postsList = [...posts.values()];
			this.locations = _(postsList)
				.filter('location_verbose')
				.countBy('location_verbose')
				.toPairs()
				.sortBy(1)
				.reverse()
				.value();

			this.tags = _(postsList)
				.map('tags')
				.flatten()
				.countBy()
				.toPairs()
				.sortBy(1)
				.reverse()
				.value();
		},

		async delete_post(id) {
			const res = await api.delete(`/posts/${id}`);
			ElNotification({
				title: 'Post deleted',
				message: 'The post has successfully been deleted.',
			});

			this.posts.delete(id);
		},

		async store_post(post) {
			const jsonData = JSON.stringify(post);
			const authStore = useAuth();
			const [nonce, data] = encrypt(authStore.masterKey, sodium.from_string(jsonData));

			const envelope = {
				nonce,
				data,
				date: post.date,
				format_version: 1,
			};

			let res;
			if (post.id) {
				res = await api.put(`/posts/${post.id}`, envelope);
			} else {
				res = await api.post('/posts', envelope);
			}

			this.posts.set(post.id, post);

			ElNotification({
				title: 'Entry saved',
				message: post.id ? 'The changes to your entry have been saved.' : 'Your entry has been saved.',
			});
		},
	},
});
