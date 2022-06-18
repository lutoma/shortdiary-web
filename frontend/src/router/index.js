import { createRouter, createWebHistory } from 'vue-router';
import { useAuth } from '@/stores/auth';

import DashboardView from '@/views/DashboardView.vue';
import TimelineView from '@/views/TimelineView.vue';
import EditPostView from '@/views/EditPostView.vue';
import NewPostView from '@/views/NewPostView.vue';
import LocationsView from '@/views/LocationsView.vue';
import PeopleView from '@/views/PeopleView.vue';
import SettingsView from '@/views/SettingsView.vue';
import LoginView from '@/views/LoginView.vue';
import JoinView from '@/views/JoinView.vue';

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'dashboard',
			component: DashboardView,
		},
		{
			path: '/posts',
			name: 'timeline',
			component: TimelineView,
		},
		{
			path: '/posts/:id/edit',
			name: 'edit-post',
			component: EditPostView,
		},
		{
			path: '/new',
			name: 'new-post',
			component: NewPostView,
		},
		{
			path: '/people',
			name: 'people',
			component: PeopleView,
		},
		{
			path: '/locations',
			name: 'locations',
			component: LocationsView,
		},
		{
			path: '/settings',
			name: 'settings',
			component: SettingsView,
		},
		{
			path: '/login',
			name: 'login',
			component: LoginView,
		},
		{
			path: '/join',
			name: 'join',
			component: JoinView,
		},
	],
});

router.beforeEach(async (to, from) => {
	const store = useAuth();

	if (!store.logged_in && !['login', 'join'].includes(to.name)) {
		return { name: 'login' };
	}
});

export default router;
