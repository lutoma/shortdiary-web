module.exports = {
	root: true,
	env: {
		es2021: true,
	},
	extends: [
		'plugin:vue/vue3-essential',
		'eslint:recommended',
		'@vue/airbnb',
	],
	rules: {
		'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
		'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
		'no-tabs': 'off',
		'max-len': 'off',
		'import/prefer-default-export': 'off',
		'arrow-body-style': 'off',
		indent: ['error', 'tab'],
		'no-unused-vars': ['warn', {
			argsIgnorePattern: '^_',
			varsIgnorePattern: '^_',
		}],

		// temp
		'no-restricted-syntax': 'off',
		'no-continue': 'off',
		'no-shadow': ['warn', { allow: ['_'] }],
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
