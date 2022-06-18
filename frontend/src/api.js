import axios from 'axios';
import { useAuth } from '@/stores/auth';
import { useRouter } from 'vue-router'

//const instance = axios.create({ baseURL: 'https://api.guardian.fnoco.eu/v1' });
const instance = axios.create({ baseURL: 'http://127.0.0.1:8000' });

instance.interceptors.request.use((config) => {
	const auth_store = useAuth();

	if (auth_store.jwt) {
		config.headers.Authorization = `Bearer ${auth_store.jwt}`;
	}

    return config;
}, (error) => { return Promise.reject(error); });


instance.interceptors.response.use(response => {
   return response;
}, (error) => {
	if(error.response) {
		if (error.response.status === 401) {
				const auth_store = useAuth();
				const router = useRouter();

				auth_store.logout();
				router.push({ name: 'login' })
		}
	}

	return Promise.reject(error);
});

export default instance;
