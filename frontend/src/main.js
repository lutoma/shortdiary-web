import { library } from '@fortawesome/fontawesome-svg-core';

import {
	faKey as faKeyRegular, faPencil as faPencilRegular, faSignIn as faSignInRegular,
	faList as faListRegular, faChartBar as faChartBarRegular, faMedal as faMedalRegular,
	faWrench as faWrenchRegular, faSignOut as faSignOutRegular, faCompass as faCompassRegular,
	faUserFriends as faUserFriendsRegular, faImages as faImagesRegular,
	faEmptySet as faEmptySetRegular, faLock as faLockRegular, faLockOpen as faLockOpenRegular,
	faBars as faBarsRegular, faFileContract as faFileContractRegular,
	faShieldCheck as faShieldCheckRegular, faSync as faSyncRegular,
	faMapMarkedAlt as faMapMarkedAltRegular, faUsers as faUsersRegular, faHouse as faHouseRegular,
} from '@fortawesome/pro-regular-svg-icons';

import {
	faLock as faLockLight, faLockOpen as faLockOpenLight, faLaugh as faLaughLight,
	faSmile as faSmileLight, faMeh as faMehLight, faFrown as faFrownLight,
	faPencil as faPencilLight, faLink as faLinkLight, faTrash as faTrashLight,
	faMapMarkedAlt as faMapMarkedAltLight, faUsers as faUsersLight,
	faChartLine as faChartLineLight, faLanguage as faLanguageLight,
	faCalendarAlt as faCalendarAltLight, faImages as faImagesLight,
	faShieldCheck as faShieldCheckLight, faTrophyAlt as faTrophyAltLight, faTally as faTallyLight,
	faRuler as faRulerLight, faTags as faTagsLight, faAlignLeft as faAlignLeftLight,
} from '@fortawesome/pro-light-svg-icons';

import { faGithub } from '@fortawesome/free-brands-svg-icons';

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import QuerySynchronizer from '@oarepo/vue-query-synchronizer';
import sodium from 'libsodium-wrappers';
import App from './App.vue';
import router from './router';

/* eslint-disable function-paren-newline, function-call-argument-newline */
library.add(faKeyRegular, faPencilRegular, faSignInRegular, faListRegular, faChartBarRegular,
	faMedalRegular, faWrenchRegular, faSignOutRegular, faCompassRegular, faUserFriendsRegular,
	faImagesRegular, faEmptySetRegular, faLockRegular, faLockOpenRegular, faBarsRegular,
	faFileContractRegular, faShieldCheckRegular, faSyncRegular, faMapMarkedAltRegular, faHouseRegular);

library.add(faLockLight, faLockOpenLight, faLaughLight, faSmileLight, faMehLight, faFrownLight,
	faPencilLight, faLinkLight, faTrashLight, faMapMarkedAltLight, faUsersLight, faChartLineLight,
	faLanguageLight, faCalendarAltLight, faImagesLight, faShieldCheckLight, faTrophyAltLight,
	faTallyLight, faRulerLight, faTagsLight, faAlignLeftLight, faUsersRegular);

library.add(faGithub);

await sodium.ready;

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);


createApp(App)
	.component('fa', FontAwesomeIcon)
	.use(pinia)
	.use(router)
	.use(QuerySynchronizer, { router: router })
	.mount('#app');
