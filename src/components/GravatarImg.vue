<template>
	<img
		v-bind="attrs"
		:src="url"
		:alt="alt"
		v-on="listeners"
		@load="onLoad"
		@error="onError"
	>
</template>

<script>
// Adapted from https://github.com/JiriChara/vue-gravatar to use local loading
import md5 from 'md5';

export default {
	name: 'GravatarImg',

	inheritAttrs: false,

	props: {
		email: {
			type: String,
			default: '',
		},

		hash: {
			type: String,
			default: '',
		},

		size: {
			type: Number,
			default: 80,
		},

		defaultImg: {
			type: String,
			default: 'mp',
		},

		rating: {
			type: String,
			default: 'g',
		},

		alt: {
			type: String,
			default: 'Avatar',
		},
	},

	computed: {
		url() {
			const img = [
				'/avatar/',
				this.hash || md5(this.email.trim().toLowerCase()),
				`?s=${this.size}`,
				`&d=${this.defaultImg}`,
				`&r=${this.rating}`,
			];

			return img.join('');
		},
		/*
			listeners() {
				const { load, error, ...listeners } = this.$listeners;

				return listeners;
			},
*/
		attrs() {
			const { src, alt, ...attrs } = this.$attrs;

			return attrs;
		},
	},

	methods: {
		onLoad(...args) {
			this.$emit('load', ...args);
		},

		onError(...args) {
			this.$emit('error', ...args);
		},
	},
};
</script>
