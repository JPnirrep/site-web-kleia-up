<?php
/**
 * KLEIA-UP - Script Sync Brevo
 * Lit les inscriptions non synchronisees et les envoie vers Brevo.
 * Usage: php php/brevo-sync.php (en CLI) ou via HTTP.
 * Rollback: Ce fichier est isole, peut etre supprime sans impact.
 */

// --- CONFIG ---
$config = include __DIR__ . '/config.php';
$apiKey = $config['brevo_api_key'];
$listId = $config['brevo_list_id'];
$dbFile = __DIR__ . '/../data/atelier-inscriptions.json';
$lockFile = __DIR__ . '/../data/brevo-sync.lock';

// --- Only CLI or authorized ---
if (PHP_SAPI !== 'cli') {
    // Accessible uniquement via token pour securite
    $token = isset($_GET['token']) ? $_GET['token'] : '';
    if ($token !== 'kleia-bravo-2026') {
        header('HTTP/1.1 403 Forbidden');
        echo "Access non autorise. Ajoutez ?token=kleia-bravo-2026";
        exit;
    }
    $isHttp = true;
} else {
    $isHttp = false;
}

// --- Output helper ---
function log_msg($msg) {
    global $isHttp;
    if ($isHttp) {
        echo $msg . "<br>\n";
    } else {
        echo $msg . "\n";
    }
    flush();
}

// --- Load DB ---
if (!file_exists($dbFile)) {
    log_msg("Aucune base de donnees trouvee. Rien a synchroniser.");
    exit;
}

$raw = file_get_contents($dbFile);
if ($raw === false) {
    log_msg("Erreur lecture DB.");
    exit(1);
}

$db = json_decode($raw, true);
if (!is_array($db)) {
    log_msg("DB corrompue.");
    exit(1);
}

// --- Filter unsynced ---
$toSync = [];
foreach ($db as $entry) {
    if (empty($entry['brevo_synced'])) {
        $toSync[] = $entry;
    }
}

if (count($toSync) === 0) {
    log_msg("Tous les contacts sont deja synchronises. (" . count($db) . " total)");
    exit;
}

log_msg("Synchronisation Brevo : " . count($toSync) . " contact(s) a envoyer...");

// --- Sync each contact ---
$synced = 0;
$failed = 0;

foreach ($toSync as &$entry) {
    $payload = [
        'email'      => $entry['email'],
        'attributes' => [
            'PRENOM' => $entry['prenom'],
            'NOM'    => $entry['nom'],
        ],
        'listIds'      => [$listId],
        'updateEnabled' => true,  // Brevo met a jour si le contact existe deja
    ];

    $ch = curl_init('https://api.brevo.com/v3/contacts');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'api-key: ' . $apiKey,
        'Content-Type: application/json',
        'Accept: application/json',
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode >= 200 && $httpCode < 300) {
        $entry['brevo_synced'] = true;
        $entry['brevo_synced_at'] = date('Y-m-d H:i:s');
        $synced++;
        log_msg("  OK  : " . $entry['email']);
    } else {
        $errBody = $response ? json_decode($response, true) : [];
        $errMsg = isset($errBody['message']) ? $errBody['message'] : "HTTP $httpCode";
        log_msg("  FAIL: " . $entry['email'] . " — " . $errMsg);
        $failed++;
    }

    // Petit delai pour eviter rate limiting
    usleep(200000); // 200ms
}

// --- Save updated DB ---
$json = json_encode($db, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
if (file_put_contents($dbFile, $json, LOCK_EX)) {
    log_msg("\nDB mise a jour. Synced: $synced, Failed: $failed");
} else {
    log_msg("\nErreur: impossible de sauvegarder la DB apres sync !");
    exit(1);
}

log_msg("Termine.");
