<template>
	<el-card class="paginated-table-card">
		<h2 v-if="title"><fa v-if="icon" :icon="['fal', icon]" /> {{ title }}</h2>
		<el-table :data="data.slice((current_page - 1) * pageSize, current_page * pageSize)" stripe>
			<slot />
		</el-table>
		<el-pagination layout="prev, pager, next" :total="data.length" :page-size="pageSize" :current-page.sync="current_page" />
	</el-card>
</template>

<script>
export default {
	props: {
		icon: { type: String, default: null },
		title: { type: String, default: null },
		data: { type: Array, required: true },
		pageSize: { type: Number, default: 10 }
	},

	data() {
		return {
			current_page: 1
		}
	}
}
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
