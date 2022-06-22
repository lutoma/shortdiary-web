import axios from 'axios';
import { useAuth } from '@/stores/auth';
import router from './router';

const BASE_URL = 'https://api.beta.shortdiary.com';
const instance = axios.create({ baseURL: BASE_URL });

instance.interceptors.request.use((_config) => {
	const config = _config;
	const store = useAuth();

	if (store.jwt) {
		const expiryRemainder = store.jwtExpiry - new Date();

		// Token expires in less than 3 days, get a new one
		if (expiryRemainder < 259200) {
			axios.post(
				`${BASE_URL}/auth/token`,
				{},
				{ headers: { Authorization: `Bearer ${store.jwt}` } }
			).then((res) => {
				store.updateToken(res.data.access_token);
			});
		}

		config.headers.Authorization = `Bearer ${store.jwt}`;
	}

	return config;
}, (error) => { return Promise.reject(error); });

instance.interceptors.response.use((response) => {
	return response;
}, (error) => {
	if (error.response) {
		if (error.response.status === 401) {
			const store = useAuth();

			store.logout(false);
			router.push({ name: 'login', query: { auto_signout: true } });
		}
	}

	return Promise.reject(error);
});

export default instance;
