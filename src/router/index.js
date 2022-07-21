import { createRouter, createWebHistory } from 'vue-router';
import { useAuth } from '@/stores/auth';

import PublicLayout from '@/layouts/PublicLayout.vue';
import DefaultLayout from '@/layouts/DefaultLayout.vue';

import DashboardView from '@/views/DashboardView.vue';
import TimelineView from '@/views/TimelineView.vue';
import LocationsView from '@/views/LocationsView.vue';
import PeopleView from '@/views/PeopleView.vue';
import SettingsView from '@/views/SettingsView.vue';
import LoginView from '@/views/LoginView.vue';
import JoinView from '@/views/JoinView.vue';
import PostEditor from '@/components/PostEditor.vue';

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '',
			name: 'default-layout',
			component: DefaultLayout,
			children: [
				{
					path: '',
					name: 'dashboard',
					component: DashboardView,
				},
				{
					path: 'posts',
					name: 'timeline',
					component: TimelineView,
					meta: {
						query: {
							text: 'string:',
							mood: 'commaarray:1,10',
							tags: 'commaarray:',
							location: 'string:',
							images: 'string:',
						},
					},
					children: [
						{
							path: 'new',
							name: 'new-post',
							component: PostEditor,
						},
						{
							path: ':id/edit',
							name: 'edit-post',
							component: PostEditor,
						},
					],
				},
				{
					path: 'people',
					name: 'people',
					component: PeopleView,
				},
				{
					path: 'places',
					name: 'locations',
					component: LocationsView,
				},
				{
					path: 'settings',
					name: 'settings',
					component: SettingsView,
				},
			],
		},
		{
			path: '',
			name: 'public-layout',
			component: PublicLayout,
			children: [
				{
					path: 'login',
					name: 'login',
					component: LoginView,
				},
				{
					path: 'join',
					name: 'join',
					component: JoinView,
				},
			],
		},
	],
});

router.beforeEach(async (to, _from) => {
	const store = useAuth();

	if (!store.logged_in && !['login', 'join'].includes(to.name)) {
		return { name: 'login' };
	}

	return true;
});

export default router;
