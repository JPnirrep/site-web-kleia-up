<?php
/**
 * KLEIA-UP - Firestore Admin Helper
 * Utilise le compte de service pour ecrire dans Firestore via REST API.
 * Usage: require_once 'firestore.php'; firestore_add('collection', $data);
 */

define('FIRESTORE_PROJECT', 'kleia-audit-jp-2026');
define('FIRESTORE_BASE', 'https://firestore.googleapis.com/v1/projects/' . FIRESTORE_PROJECT . '/databases/(default)/documents');

/**
 * Obtient un token OAuth2 a partir du compte de service.
 */
function firestore_token() {
    $credFile = __DIR__ . '/firebase-credentials.json';
    if (!file_exists($credFile)) return null;

    $cred = json_decode(file_get_contents($credFile), true);
    if (!$cred) return null;

    // Construire le JWT
    $header = base64url(json_encode(['alg' => 'RS256', 'typ' => 'JWT']));
    $now = time();
    $payload = base64url(json_encode([
        'iss'   => $cred['client_email'],
        'scope' => 'https://www.googleapis.com/auth/datastore',
        'aud'   => $cred['token_uri'],
        'exp'   => $now + 3600,
        'iat'   => $now,
    ]));

    $toSign = "$header.$payload";
    $pkey = openssl_get_privatekey($cred['private_key']);
    if (!$pkey) return null;

    openssl_sign($toSign, $signature, $pkey, 'SHA256');
    openssl_free_key($pkey);

    $jwt = $toSign . '.' . base64url($signature);

    // Echanger JWT contre token
    $ch = curl_init($cred['token_uri']);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query([
            'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion'  => $jwt,
        ]),
        CURLOPT_HTTPHEADER => ['Content-Type: application/x-www-form-urlencoded'],
        CURLOPT_TIMEOUT => 10,
    ]);
    $resp = curl_exec($ch);
    curl_close($ch);

    $data = json_decode($resp, true);
    return isset($data['access_token']) ? $data['access_token'] : null;
}

/**
 * Ajoute un document dans une collection Firestore.
 * Retourne l'ID du document cree ou false en cas d'echec.
 */
function firestore_add($collection, $data) {
    $token = firestore_token();
    if (!$token) return false;

    // Transformer les donnees en format Firestore REST
    $fields = [];
    foreach ($data as $key => $value) {
        if (is_bool($value)) {
            $fields[$key] = ['booleanValue' => $value];
        } elseif (is_int($value) || is_float($value)) {
            $fields[$key] = ['integerValue' => $value];
        } elseif ($value === null) {
            $fields[$key] = ['nullValue' => null];
        } else {
            $fields[$key] = ['stringValue' => (string) $value];
        }
    }

    $url = FIRESTORE_BASE . '/' . $collection;
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode(['fields' => $fields]),
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $token,
            'Content-Type: application/json',
        ],
        CURLOPT_TIMEOUT => 10,
    ]);
    $resp = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($code >= 200 && $code < 300) {
        $doc = json_decode($resp, true);
        // Extraire l'ID depuis le nom (format: projects/.../documents/collection/docId)
        $parts = explode('/', $doc['name']);
        return end($parts);
    }

    return false;
}

/**
 * Helper: encodage base64url (RFC 7515)
 */
function base64url($data) {
    return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}
