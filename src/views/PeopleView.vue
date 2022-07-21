<template>
	<div class="people">
		<h1>People</h1>

		<el-row :gutter="30">
			<el-col v-for="mention in store.mentions" :key="mention[0]" :span="6">
				<el-card>
					<h4>{{ mention[0].slice(1) }}</h4>
					<p>
						<router-link :to="{ name: 'timeline', query: { text: mention[0] } }">
							Mentioned in {{ mention[1] }} posts
						</router-link>
					</p>
				</el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script setup>
import { usePosts } from '@/stores/posts';

const store = usePosts();
store.load();
</script>

<style lang="scss">
.people {
	.el-card {
		margin-bottom: 30px;

		h4 {
			text-transform: capitalize;
		}
	}
}
</style>
