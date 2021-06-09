// Safely retrieve a field error from a DRF error dict
export function get_error(field) {
	if (!this.error || !(field in this.error)) {
		return null
	}

	return this.error[field].join(', ')
}
