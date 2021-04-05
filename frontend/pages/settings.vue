<template>
	<div class="settings">
		<h1>Settings</h1>

		<el-row :gutter="50">
			<el-col :span="12">
				<el-card>
					<h2>Account settings</h2>
					<el-form ref="form" :model="form" label-width="160px">
						<el-form-item label="Username">
							<el-input v-model="user.username" />
						</el-form-item>
						<el-form-item label="Email">
							<el-input v-model="user.email" />
						</el-form-item>
						<el-form-item label="New password">
							<el-input v-model="form.password" show-password />
						</el-form-item>
						<el-form-item label="New password (repeat)">
							<el-input v-model="form.password_repeat" show-password />
						</el-form-item>
					</el-form>
				</el-card>
			</el-col>

			<el-col :span="12">
				<el-card>
					<h2>Notification settings</h2>

					<el-form ref="form" :model="form" label-width="160px">
						<el-form-item label="Email notifications">
							<el-checkbox-group v-model="form.type">
								<el-checkbox label="Streak reminders" name="type" />
								<el-checkbox label="Past memories" name="type" />
							</el-checkbox-group>
						</el-form-item>
					</el-form>
				</el-card>
			</el-col>

			<el-col :span="12">
				<el-card>
					<h2>Post settings</h2>
					<el-form ref="form" :model="form" label-width="160px">
						<el-form-item label="Default post visibility">
							<el-select v-model="form.region" placeholder="please select your zone">
								<el-option label="Zone one" value="shanghai"></el-option>
								<el-option label="Zone two" value="beijing"></el-option>
							</el-select>
						</el-form-item>
						<el-form-item label="Include locations">
							<el-switch v-model="form.delivery"></el-switch>
						</el-form-item>
					</el-form>
				</el-card>
			</el-col>
		</el-row>

		<el-button type="primary" @click="onSubmit">Save settings</el-button>
	</div>
</template>


<script>
	export default {
		data() {
			let data = {
				form: {
					name: '',
					region: '',
					date1: '',
					date2: '',
					delivery: false,
					type: [],
					resource: '',
					desc: '',
					password: '',
					password_repeat: '',
				}
			}

			data['user'] = this.$auth.user
			return data
		},
		methods: {
			onSubmit() {
				console.log('submit!');
			}
		}
	}
</script>

<style>
.settings .el-card {
	margin-bottom: 30px;
}
</style>
