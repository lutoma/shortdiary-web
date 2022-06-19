import sodium from 'libsodium-wrappers';

function deriveKey(password, b64Salt) {
	const salt = sodium.from_base64(b64Salt);
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

function splitKey(key) {
/*	const passwordKey = key.slice(0, sodium.crypto_secretbox_KEYBYTES)
	const authToken = key.slice(sodium.crypto_secretbox_KEYBYTES, sodium.crypto_secretbox_KEYBYTES * 2)
	return [passwordKey, authToken]
*/
	return [key, key];
}

export function encrypt(key, data) {
	const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
	const cryptData = sodium.crypto_secretbox_easy(data, nonce, key);
	return [sodium.to_base64(nonce), sodium.to_base64(cryptData)];
}

export function decrypt(key, b64Nonce, b64CryptData) {
	const nonce = sodium.from_base64(b64Nonce);
	const cryptData = sodium.from_base64(b64CryptData);
	return sodium.crypto_secretbox_open_easy(cryptData, nonce, key);
}

export function enrol(password) {
	const salt = sodium.to_base64(sodium.randombytes_buf(sodium.crypto_pwhash_SALTBYTES));
	const ephemeralKey = deriveKey(password, salt);
	const key = sodium.crypto_secretbox_keygen();
	const [passwordKey, authToken] = splitKey(ephemeralKey);
	const [nonce, encryptedKey] = encrypt(passwordKey, key);
	return [salt, nonce, encryptedKey];
}

export function unlock(password, salt, masterNonce, encryptedMaster) {
	const ephemeralKey = deriveKey(password, salt);
	const [passwordKey, authToken] = splitKey(ephemeralKey);
	return decrypt(passwordKey, masterNonce, encryptedMaster);
}
