import sodium from 'libsodium-wrappers';

function derive_key(password, b64_salt) {
	const salt = sodium.from_base64(b64_salt);
	return sodium.crypto_pwhash(
	//	sodium.crypto_secretbox_KEYBYTES * 2,
		sodium.crypto_secretbox_KEYBYTES,
		password,
		salt,
		10,
		30 * (1024 ** 2),
		sodium.crypto_pwhash_ALG_ARGON2ID13,
	);
}

function split_key(key) {
/*	const password_key = key.slice(0, sodium.crypto_secretbox_KEYBYTES)
	const auth_token = key.slice(sodium.crypto_secretbox_KEYBYTES, sodium.crypto_secretbox_KEYBYTES * 2)
	return [password_key, auth_token]
*/
	return [key, key];
}

export function encrypt(key, data) {
	const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
	const crypt_data = sodium.crypto_secretbox_easy(data, nonce, key);
	return [sodium.to_base64(nonce), sodium.to_base64(crypt_data)];
}

export function decrypt(key, b64nonce, b64crypt_data) {
	const nonce = sodium.from_base64(b64nonce);
	const crypt_data = sodium.from_base64(b64crypt_data);
	return sodium.crypto_secretbox_open_easy(crypt_data, nonce, key);
}

export function enrol(password) {
	const salt = sodium.to_base64(sodium.randombytes_buf(sodium.crypto_pwhash_SALTBYTES));
	const ephemeral_key = derive_key(password, salt);
	const key = sodium.crypto_secretbox_keygen();
	const [password_key, auth_token] = split_key(ephemeral_key);
	const [nonce, encrypted_key] = encrypt(password_key, key);
	return [salt, nonce, encrypted_key];
}

export function unlock(password, salt, master_nonce, encrypted_master) {
	const ephemeral_key = derive_key(password, salt);
	const [password_key, auth_token] = split_key(ephemeral_key);
	return decrypt(password_key, master_nonce, encrypted_master);
}
