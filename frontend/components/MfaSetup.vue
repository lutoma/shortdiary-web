<template>
	<div class="mfa-setup" v-loading="!config.methods.length">
		<el-alert class="error" v-if="error" :title="error" :closable="false" type="error" />

		<template v-if="step === 'method_select'">
			<p>Select a method:</p>

			<div class="input-group">
				<el-select v-model="selected_method" placeholder="Select">
					<el-option v-for="item in available_methods" :key="item[0]" :label="item[1]" :value="item[0]" />
				</el-select>
				<el-button type="primary" @click="selectMethod">Continue</el-button>
			</div>
		</template>

		<template v-if="step === 'phone_number'">
			<p>Please enter your phone number:</p>

			<div class="input-group">
				<el-input placeholder="Phone number" v-model="phone_number" />
				<el-button type="primary" @click="addPhoneNumber">Confirm</el-button>
			</div>
		</template>

		<div v-if="step === 'confirmation'">
			<template v-if="selected_method == 'app'">
				<p>Please scan the QR code with your mobile authenticator app, then enter the generated code below for confirmation.</p>
				<qrcode-vue class="qr" :value="confirmation.qr_link" :size="175"></qrcode-vue>
			</template>
			<template v-if="selected_method == 'sms'">
				<p>Please enter the code you have received by text message</p>
			</template>

			<div class="input-group">
				<el-input placeholder="Code" v-model="code" />
				<el-button type="primary" @click="confirmMethod">Confirm</el-button>
			</div>
		</div>
	</div>
</template>

<script>
import QrcodeVue from 'qrcode.vue'

export default {
	components: {
		QrcodeVue
	},

	props: {
		config: { type: Object, default: { methods: [] } },
		active_methods: { type: Array, default: [] }
	},

	data() {
		return {
			step: 'method_select',
			selected_method: null,
			confirmation: null,
			phone_number: '',
			code: '',
			error: null
		}
	},

	computed: {
		available_methods() {
			const active_names = this.active_methods.map(a => a.name)
			return this.config.methods.filter(el => !active_names.includes(el[0]))
		}
	},

	methods: {
		async selectMethod() {
			// Continue directly to activation when method is 'app',
			// show phone number input for 'sms'
			if (this.selected_method === 'app') {
				this.activateMethod()
			} else {
				this.step = 'phone_number'
			}
		},

		async addPhoneNumber() {
			await this.$axios.$patch('/user/', { phone_number: this.phone_number })
			this.activateMethod()
		},

		async activateMethod() {
			this.error = null

			try {
				this.confirmation = await this.$axios.$post(
					`/auth/${this.selected_method}/activate/`,
					{ method: this.selected_method }
				)

				this.step = 'confirmation'
			} catch (err) {
				this.error = err.response.data.error
			}
		},

		async confirmMethod() {
			this.error = null

			try {
				await this.$axios.$post(
					`/auth/${this.selected_method}/activate/confirm/`,
					{ method: this.selected_method, code: this.code }
				)

				this.step = 'method_select'
				this.$emit('success')
			} catch (err) {
				this.error = err.response.data.non_field_errors[0]
			}
		}
	}
}
</script>

<style lang="scss">
.mfa-setup {
	.error {
		margin-bottom: 1rem;
	}

	p {
		margin-top: 0;
		word-break: break-word;
	}

	.input-group {
		display: flex;
		flex-direction: row;

		* {
			flex-grow: 1;
		}

		button {
			flex-grow: 0;
			width: 100px;
			margin-left: .5rem;
		}
	}

	.qr {
		display: flex;
		flex-direction: row;
		justify-content: center;
		margin-bottom: 1.5rem;
	}
}
</style>
