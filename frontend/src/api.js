import axios from 'axios';
import { useAuth } from '@/stores/auth';
import router from './router';

const instance = axios.create({ baseURL: 'https://api.beta.shortdiary.com' });

instance.interceptors.request.use((_config) => {
	const config = _config;
	const store = useAuth();

	if (store.jwt) {
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
