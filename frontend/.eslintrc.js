module.exports = {
	root: true,
	env: {
		es2021: true,
	},
	extends: [
		'plugin:vue/vue3-recommended',
		'eslint:recommended',
		'@vue/airbnb',
	],
	rules: {
		'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
		'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',

		'no-tabs': 'off',
		indent: ['error', 'tab'],
		'vue/html-indent': ['error', 'tab'],

		'max-len': 'off',
		'import/prefer-default-export': 'off',
		'arrow-body-style': 'off',
		'vue/max-attributes-per-line': 'off',
		'vue/multi-word-component-names': 'off',

		'no-unused-vars': ['warn', {
			argsIgnorePattern: '^_',
			varsIgnorePattern: '^_',
		}],
		'vue/no-unused-vars': ['warn', { ignorePattern: '^_' }],
		'no-shadow': ['warn', { allow: ['_'] }],

		// temp
		'no-restricted-syntax': 'off',
		'no-continue': 'off',
	},

	settings: {
		'import/resolver': {
			alias: {
				map: [
					['@', './src'],
				],
			},
		},
	},
};
