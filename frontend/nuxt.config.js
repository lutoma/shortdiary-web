export default {
	head: {
		title: 'shortdiary',
		htmlAttrs: {
			lang: 'en'
		},
		meta: [
			{ charset: 'utf-8' },
			{ name: 'viewport', content: 'width=device-width, initial-scale=1' },
			{ name: 'apple-mobile-web-app-capable', content: 'yes' },

			{ name: 'application-name', content: 'Shortdiary' },
			{ name: 'msapplication-TileColor', content: '#036564' },
			{ name: 'msapplication-square70x70logo', content: '/windows-tile-tiny.png' },
			{ name: 'msapplication-square150x150logo', content: '/windows-tile-square.png' },
			{ name: 'msapplication-wide310x150logo', content: '/windows-tile-wide.png' },
			{ name: 'msapplication-square310x310logo', content: '/windows-tile-large.png' }
		],

		link: [
			{ rel: 'icon', type: 'image/png', href: '/favicon.png' },
			{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },

			{ rel: 'apple-touch-icon', sizes: '57x57', href: '/apple-touch-icon-114.png' },
			{ rel: 'apple-touch-icon', sizes: '114x114', href: '/apple-touch-icon-114.png' },
			{ rel: 'apple-touch-icon', sizes: '72x72', href: '/apple-touch-icon-144.png' },
			{ rel: 'apple-touch-icon', sizes: '144x144', href: '/apple-touch-icon-144.png' },
			{ rel: 'apple-touch-icon', href: '/apple-touch-icon-114.png' }

		]
	},

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
		'@nuxtjs/proxy'
	],

	build: {
		transpile: [/^element-ui/],
		hotMiddleware: {
			client: {
				overlay: false
			}
		},

		// Needed for dynamic template in Post.vue
		extend(config) {
			config.resolve.alias.vue = 'vue/dist/vue.common'
		}
	},

	render: {
		csp: {
			hashAlgorithm: 'sha256',
			policies: {
				'script-src': ["'unsafe-eval'", 'blob:', 'https://hcaptcha.com', 'https://*.hcaptcha.com'],
				'frame-src': ['https://hcaptcha.com', 'https://*.hcaptcha.com'],
				'style-src': ["'self'", "'unsafe-inline'", 'https://hcaptcha.com', 'https://*.hcaptcha.com'],
				'connect-src': ["'self'", 'https://api.shortdiary.com', 'https://hcaptcha.com', 'https://*.hcaptcha.com']
			}
		}
	},

	router: {
		middleware: ['auth']
	},

	// Proxy external services to avoid leaking user IPs
	proxy: {
		'/map/': {
			target: 'https://api.mapbox.com',
			pathRewrite: { '^/map/': '' }
		},
		'/avatar/': 'https://www.gravatar.com/'
	},

	axios: {
		baseURL: 'https://api.shortdiary.com/v2'
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
			home: '/dashboard'
		},
		cookie: {
			options: {
				maxAge: 604800
			}
		}
	},

	fontawesome: {
		component: 'fa',
		proIcons: {
			regular: [
				'faKey',
				'faPencil',
				'faSignIn',
				'faList',
				'faChartBar',
				'faMedal',
				'faWrench',
				'faSignOut',
				'faCompass',
				'faUserFriends',
				'faImages',
				'faEmptySet',
				'faLock',
				'faLockOpen'
			],
			light: [
				'faLock',
				'faLockOpen',
				'faLaugh',
				'faSmile',
				'faMeh',
				'faFrown',
				'faPencil',
				'faLink',
				'faTrash',
				'faMapMarkedAlt',
				'faUsers',
				'faChartLine',
				'faLanguage'
			]
		}
	}
}
