import { defineStore } from 'pinia';
import { AxiosError } from 'axios';
import { enrol, unlock } from '@/crypto';
import { ElNotification } from 'element-plus';
import cloneDeep from 'lodash/cloneDeep';
import api from '@/api';

export const useAuth = defineStore('auth', {
	state: () => {
		return {
			masterKey: null,
			jwt: null,
			jwtExpiry: null,
			user: null,
		};
	},

	getters: {
		logged_in: (state) => state.jwt !== null && state.masterKey !== null,
		haveSubscription: (state) => {
			const subStatus = state.user?.subscription?.status;
			return subStatus === 'active';
		},
	},

	actions: {
		async updateToken(jwt) {
			const jwtData = JSON.parse(atob(jwt.split('.')[1]));
			this.jwtExpiry = new Date(jwtData.exp * 1000);
			this.jwt = jwt;
		},

		async login(email, password) {
			const credentials = new FormData();
			credentials.append('username', email);
			credentials.append('password', password);

			try {
				const res = await api.post('/auth/login', credentials);
				await this.updateToken(res.data.access_token);
				this.user = res.data.user;

				if (this.user.master_key) {
					this.masterKey = await unlock(password, this.user.ephemeral_key_salt, this.user.master_key_nonce, this.user.master_key);
				} else {
					const [ephemeralKeySalt, masterKeyNonce, masterKey] = await enrol(password);

					const userData = cloneDeep(this.user);
					delete userData.id;
					delete userData.subscription;

					await api.put('/auth/user', {
						...userData,
						ephemeral_key_salt: ephemeralKeySalt,
						master_key_nonce: masterKeyNonce,
						master_key: masterKey,
					});

					this.masterKey = await unlock(password, ephemeralKeySalt, masterKeyNonce, masterKey);
				}
			} catch (err) {
				if (err instanceof AxiosError && err.response) {
					throw err.response.data.detail;
				} else {
					throw err;
				}
			}
		},

		async logout(notification = true) {
			this.$reset();

			if (notification) {
				ElNotification({
					title: 'Signed out',
					message: 'You have successfully been signed out.',
				});
			}
		},

		async signup(user) {
			const [ephemeralKeySalt, masterKeyNonce, masterKey] = await enrol(user.password);

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

		async updateUser(user) {
			try {
				const res = await api.put('/auth/user', user);
				this.user = res.data;
			} catch (err) {
				if (err instanceof AxiosError && err.response) {
					throw err.response.data.detail;
				} else {
					throw err;
				}
			}

			ElNotification({
				title: 'Settings saved',
				message: 'The changes to your settings have been saved.',
			});
		},

		async loadUser() {
			try {
				const res = await api.get('/auth/user');
				this.user = res.data;
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

			if (store.jwtExpiry) {
				store.jwtExpiry = new Date(store.jwtExpiry);
			}
		},
	},
});
