export default {
	head: {
		title: 'shortdiary',
		htmlAttrs: {
			lang: 'en'
		},
		meta: [
			{ charset: 'utf-8' },
			{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
			{ hid: 'description', name: 'description', content: '' }
		],
		link: [
			{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
		]
	},

	css: [
		'element-ui/lib/theme-chalk/index.css'
	],

	plugins: [
		'@/plugins/element-ui'
	],

	components: true,

	buildModules: [
		'@nuxtjs/eslint-module',
		'@nuxtjs/fontawesome'
	],

	modules: [
		'@nuxtjs/axios',
		'@nuxtjs/auth-next',
		'@nuxtjs/proxy',
		'nuxt-leaflet'
	],

	build: {
		transpile: [/^element-ui/],
		hotMiddleware: {
			client: {
				overlay: false
			}
		}
	},

	router: {
		middleware: ['auth']
	},

	// Proxy external services to avoid leaking user IPs
	proxy: {
		'/map/tiles/**/*.png': {
			target: 'https://api.maptiler.com/maps/bright',
			pathRewrite: { '^/map/tiles': '' },
			onProxyReq: (proxyReq, req, res) => {
				proxyReq.path += '?key=bfo60JdkhRcsQQlWkLEc'
			}
		},
		'/avatar/': 'https://www.gravatar.com/'
	},

	axios: {
		// baseURL: 'https://api.shortdiary.me/v2',
		baseURL: 'http://10.35.22.2:8000/api/v2'
	},

	auth: {
		strategies: {
			local: {
				token: {
					property: 'key',
					type: 'Token'
				},
				user: {
					property: false,
					autoFetch: true
				},
				endpoints: {
					login: { url: '/auth/login/', method: 'post' },
					logout: { url: '/auth/logout/', method: 'post' },
					user: { url: '/user/', method: 'get' }
				}
			}
		},
		redirect: {
			login: '/login',
			logout: '/login',
			callback: '/',
			home: '/'
		}
	},

	fontawesome: {
		component: 'fa',
		proIcons: {
			regular: [
				'faLock',
				'faLockOpen',
				'faKey',
				'faPencil',
				'faSignIn',
				'faColumns',
				'faChartBar',
				'faMedal',
				'faWrench',
				'faSignOut',
				'faCompass',
				'faUserFriends'
			]
		}
	}
}
