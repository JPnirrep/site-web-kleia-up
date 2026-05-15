<?php
/**
 * KLEIA-UP - Brevo Push (automatique)
 * Appele a chaque inscription pour sync immediate vers Brevo.
 * Appele par le popup JS (atelier-popup.js).
 */

header('Content-Type: application/json; charset=utf-8');

// --- CONFIG ---
$config = include __DIR__ . '/config.php';
$apiKey = $config['brevo_api_key'];
$listId = $config['brevo_list_id'];

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'POST requis.']);
    exit;
}

$prenom = isset($_POST['prenom']) ? trim($_POST['prenom']) : '';
$nom    = isset($_POST['nom'])    ? trim($_POST['nom'])    : '';
$email  = isset($_POST['email'])  ? trim($_POST['email'])  : '';

if (empty($prenom) || empty($nom) || empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['status' => 'error', 'message' => 'Donnees invalides.']);
    exit;
}

$payload = json_encode([
    'email'      => strtolower($email),
    'attributes' => [
        'PRENOM' => $prenom,
        'NOM'    => $nom,
    ],
    'listIds'       => [$listId],
    'updateEnabled' => true,
]);

$ch = curl_init('https://api.brevo.com/v3/contacts');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'api-key: ' . $apiKey,
    'Content-Type: application/json',
    'Accept: application/json',
]);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode >= 200 && $httpCode < 300) {
    echo json_encode(['status' => 'success', 'message' => 'Contact synced.']);
} else {
    $err = json_decode($response, true);
    $msg = isset($err['message']) ? $err['message'] : "HTTP $httpCode";
    echo json_encode(['status' => 'error', 'message' => $msg]);
}
