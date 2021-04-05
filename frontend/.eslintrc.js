module.exports = {
	root: true,
	env: {
		browser: true,
		node: true
	},

	parserOptions: {
		parser: 'babel-eslint',
		ecmaVersion: 11
	},

	extends: [
		'standard'
		// 'plugin:vue/recommended'
	],

	plugins: [
		'vue'
	],

	rules: {
		indent: ['error', 'tab'],
		'vue/html-indent': ['error', 'tab'],
		'vue/max-attributes-per-line': 'off',
		'vue/attributes-order': 'off',
		'no-tabs': 0,
		'space-before-function-paren': 0,
		camelcase: 0
	}
}
