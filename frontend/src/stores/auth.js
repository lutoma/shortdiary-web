import { defineStore } from 'pinia';
import { AxiosError } from 'axios';
import { enrol, unlock } from '@/crypto';
import api from '@/api';

export const useAuth = defineStore('auth', {
	state: () => {
		return {
			master_key: null,
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
				this.master_key = unlock(password, res.data.ephemeral_key_salt, res.data.master_key_nonce, res.data.master_key);

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
			const [ephemeral_key_salt, master_key_nonce, master_key] = enrol(user.password);

			const data = {
				...user,
				ephemeral_key_salt,
				master_key_nonce,
				master_key,
			};

			const res = await api.post('/auth/signup', data);
		},
	},

	persist: {
		key: 'shortdiary-auth',
		afterRestore: ({ store }) => {
			// Store gets serialized as JSON in localStorage, which cannot deal with the Uint8Array
			// and turns it into an Object instead. So we need to manually restore it
			if (store.master_key) {
				store.master_key = Uint8Array.from(Object.values(store.master_key));
			}
		},
	},
});
