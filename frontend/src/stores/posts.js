import { defineStore } from 'pinia';
import { useAuth } from './auth';
import api from '@/api';
import _ from 'lodash'
import { decrypt } from '@/crypto'
import sodium from 'libsodium-wrappers'

export const usePosts = defineStore('post', {
	state: () => {
		return {
			posts: [],
			top_mentions: [],
			top_locations: [],
			top_tags: []
		};
	},

	actions: {
		async load() {
			const auth_store = useAuth();
			if (!auth_store.master_key) {
				return
			}

			const res = await api.get('/posts');

			await sodium.ready
			const posts = []
			for (const cpost of res.data) {
				let post_data = null

				switch (cpost.format_version) {
				case 0:
					// Unencrypted legacy posts
					post_data = cpost.data
					break
				case 1:
					try {
						post_data = sodium.to_string(decrypt(auth_store.master_key, cpost.nonce, cpost.data))
					} catch(err) {
						console.error(`Could not decrypt post ${cpost.id}: ${err.toString()}`);
						continue;
					}
					break
				default:
					console.error('Unknown post format version', cpost.format_version)
					continue
				}

				posts.push(JSON.parse(post_data))
			}

			this.posts = posts

			// Extract top mentions for use in stats.vue and PostEditor component
			const mentions = []
			for (const post of posts) {
				// FIXME Should deduplicate/DRYfy regex with Post.vue
				// Temporarily cast to Set to deduplicate mentions within a post
				mentions.push(...[...new Set(post.text.toLowerCase().match(/@\w+\b/g))])
			}

			this.top_mentions = _(mentions)
				.countBy()
				.toPairs()
				.sortBy(1)
				.reverse()
				.value()

			this.top_locations = _(posts)
				.filter('location_verbose')
				.countBy('location_verbose')
				.toPairs()
				.sortBy(1)
				.reverse()
				.value()

			this.top_tags = _(posts)
				.map('tags')
				.flatten()
				.countBy()
				.toPairs()
				.sortBy(1)
				.reverse()
				.value()
		},
	},
});
