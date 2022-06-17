import { defineStore } from 'pinia';
import api from '@/api';
import _ from 'lodash'
import { enrol as crypto_enrol, unlock as crypto_unlock } from '@/crypto'
import sodium from 'libsodium-wrappers'

export const useAuth = defineStore('auth', {
	state: () => {
		return {
			master_key: null,
			jwt: null,
		};
	},

	getters: {
		logged_in: (state) => state.jwt !== null,
	},

	actions: {
		async login(email, password) {
			const credentials = new FormData();
			credentials.append('username', email);
			credentials.append('password', password);

			const res = await api.post('/auth/login', credentials);

			await sodium.ready
			this.master_key = crypto_unlock(password, res.data.ephemeral_key_salt, res.data.master_key_nonce, res.data.master_key);
			this.jwt = res.data.access_token;
		},

		async signup(user) {
			await sodium.ready
			const [ephemeral_key_salt, master_key_nonce, master_key] = crypto_enrol(user.password)

			const data = {
				...user,
				ephemeral_key_salt,
				master_key_nonce,
				master_key,
			}

			const res = await api.post('/auth/signup', data)
		}
	},
});
