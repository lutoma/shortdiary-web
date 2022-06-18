<template>
	<fa :icon="[weight, icon]" />
</template>

<script>
export default {
	props: {
		weight: { type: String, default: 'fal' },
		mood: { type: Number, required: true },
	},

	computed: {
		icon() {
			if (this.mood <= 3) {
				return 'frown';
			}

			if (this.mood >= 6 && this.mood <= 8) {
				return 'smile';
			}

			if (this.mood >= 9) {
				return 'laugh';
			}

			return 'meh';
		},
	},
};
</script>
