<template>
	<el-row class="equal-height-row" :gutter="gutter" :style="{ '--equal-height-row-gutter': `${gutter}px` }">
		<slot />
	</el-row>
</template>

<script setup>
defineProps({ gutter: { type: Number, default: 80 } });
</script>

<style lang="scss">
.equal-height-row {
	display: flex;
	flex-wrap: wrap;

	.el-col {
		margin-bottom: var(--equal-height-row-gutter);

		> :first-child {
			height: 100%;
		}
	}
}
</style>
