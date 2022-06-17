import axios from 'axios';
import { useAuth } from '@/stores/auth';

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
/*
	if(error.response) {
		if (error.response.status === 401) {
			localStorage.removeItem('guardian_token');

			// FIXME refresh token / redirect to login here
		}
	}
*/
	return Promise.reject(error);
});

export default instance;
