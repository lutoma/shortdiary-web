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

export async function encrypt(key, data) {
	await sodium.ready;
	const nonce = await sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
	const cryptData = await sodium.crypto_secretbox_easy(data, nonce, key);
	return [sodium.to_base64(nonce), sodium.to_base64(cryptData)];
}

export async function decrypt(key, b64Nonce, b64CryptData) {
	await sodium.ready;
	const nonce = await sodium.from_base64(b64Nonce);
	const cryptData = await sodium.from_base64(b64CryptData);
	return sodium.crypto_secretbox_open_easy(cryptData, nonce, key);
}

export async function enrol(password) {
	await sodium.ready;
	const salt = await sodium.to_base64(sodium.randombytes_buf(sodium.crypto_pwhash_SALTBYTES));
	const ephemeralKey = await deriveKey(password, salt);
	const key = await sodium.crypto_secretbox_keygen();
	const [passwordKey, authToken] = await splitKey(ephemeralKey);
	const [nonce, encryptedKey] = await encrypt(passwordKey, key);
	return [salt, nonce, encryptedKey];
}

export async function unlock(password, salt, masterNonce, encryptedMaster) {
	await sodium.ready;
	const ephemeralKey = await deriveKey(password, salt);
	const [passwordKey, authToken] = await splitKey(ephemeralKey);
	return decrypt(passwordKey, masterNonce, encryptedMaster);
}
