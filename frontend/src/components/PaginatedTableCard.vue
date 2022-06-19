<template>
	<el-card class="paginated-table-card">
		<h2 v-if="title"><fa v-if="icon" :icon="['fal', icon]" /> {{ title }}</h2>
		<el-table :data="data.slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe>
			<slot />
		</el-table>
		<el-pagination layout="prev, pager, next" :total="data.length" :page-size="pageSize" v-model:current-page="currentPage" />
	</el-card>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
	icon: { type: String, default: null },
	title: { type: String, default: null },
	data: { type: Array, required: true },
	pageSize: { type: Number, default: 10 },
});

const currentPage = ref(1);
</script>

<style lang="scss">
.paginated-table-card {
	.el-card__body {
		height: 100%;
		display: flex;
		flex-direction: column;
	}

	.el-table {
		flex-grow: 1;
	}
}
</style>
