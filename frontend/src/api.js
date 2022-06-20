import axios from 'axios';
import { useAuth } from '@/stores/auth';
import { useRouter } from 'vue-router';
import { ElNotification } from 'element-plus';

// const instance = axios.create({ baseURL: 'https://api.guardian.fnoco.eu/v1' });
const instance = axios.create({ baseURL: 'http://127.0.0.1:8000' });

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
			const router = useRouter();

			store.logout(false);

			ElNotification({
				title: 'Automatically signed out',
				message: 'You have been signed out due to inactivity. Please sign in again.',
			});

			if (router) {
				router.push({ name: 'login' });
			}
		}
	}

	return Promise.reject(error);
});

export default instance;
