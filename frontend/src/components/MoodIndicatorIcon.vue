<template>
	<fa :icon="[weight, icon]" />
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
	weight: { type: String, default: 'fal' },
	mood: { type: Number, required: true },
});

const icon = computed(() => {
	if (props.mood <= 3) {
		return 'frown';
	}

	if (props.mood >= 6 && props.mood <= 8) {
		return 'smile';
	}

	if (props.mood >= 9) {
		return 'laugh';
	}

	return 'meh';
});
</script>
