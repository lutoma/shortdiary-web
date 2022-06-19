import { defineStore } from 'pinia';
import { AxiosError } from 'axios';
import { enrol, unlock } from '@/crypto';
import api from '@/api';

export const useAuth = defineStore('auth', {
	state: () => {
		return {
			masterKey: null,
			jwt: null,
			name: '',
			email: '',
		};
	},

	getters: {
		logged_in: (state) => state.jwt !== null && state.master_key !== null,
	},

	actions: {
		async login(email, password) {
			const credentials = new FormData();
			credentials.append('username', email);
			credentials.append('password', password);

			try {
				const res = await api.post('/auth/login', credentials);
				this.masterKey = unlock(password, res.data.ephemeral_key_salt, res.data.master_key_nonce, res.data.master_key);

				this.jwt = res.data.access_token;
				this.name = res.data.name;
				this.email = res.data.email;
			} catch (err) {
				if (err instanceof AxiosError && err.response) {
					throw err.response.data.detail;
				} else {
					throw err;
				}
			}
		},

		async logout() {
			this.$reset();
		},

		async signup(user) {
			const [ephemeralKeySalt, masterKeyNonce, masterKey] = enrol(user.password);

			try {
				await api.post('/auth/signup', {
					...user,
					ephemeral_key_salt: ephemeralKeySalt,
					master_key_nonce: masterKeyNonce,
					master_key: masterKey,
				});
			} catch (err) {
				if (err instanceof AxiosError && err.response) {
					throw err.response.data.detail;
				} else {
					throw err;
				}
			}
		},
	},

	persist: {
		key: 'shortdiary-auth',
		afterRestore: (ctx) => {
			const { store } = ctx;

			// Store gets serialized as JSON in localStorage, which cannot deal with the Uint8Array
			// and turns it into an Object instead. So we need to manually restore it
			if (store.masterKey) {
				store.masterKey = Uint8Array.from(Object.values(store.masterKey));
			}
		},
	},
});
