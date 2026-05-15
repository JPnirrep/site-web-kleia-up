<?php
/**
 * KLEIA-UP - Endpoint Inscription Atelier "Prendre sa place sans forcer"
 * Deployment: v1.0 - Mini-DB JSON + RGPD Consent
 * Rollback: Ce fichier peut etre supprime sans impact sur le reste du site.
 */

header('Content-Type: application/json; charset=utf-8');

// --- CONFIG ---
$db_dir = __DIR__ . '/../data';
$db_file = $db_dir . '/atelier-inscriptions.json';
$db_lock = $db_dir . '/atelier-subscribe.lock';

// --- HELPER: safe JSON read ---
function load_db($path) {
    if (!file_exists($path)) {
        return [];
    }
    $raw = file_get_contents($path);
    if ($raw === false) {
        return [];
    }
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}

// --- HELPER: safe JSON write with lock ---
function save_db($path, $lock_path, $data) {
    $dir = dirname($path);
    if (!is_dir($dir)) {
        if (!mkdir($dir, 0755, true)) {
            return false;
        }
    }

    $fp = fopen($lock_path, 'c');
    if (!$fp) return false;
    if (!flock($fp, LOCK_EX)) {
        fclose($fp);
        return false;
    }

    $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    $written = file_put_contents($path, $json, LOCK_EX);

    flock($fp, LOCK_UN);
    fclose($fp);

    return $written !== false;
}

// --- Only POST ---
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'Methode non autorisee.']);
    exit;
}

// --- Input ---
$prenom = isset($_POST['prenom']) ? strip_tags(trim($_POST['prenom'])) : '';
$nom    = isset($_POST['nom'])    ? strip_tags(trim($_POST['nom']))    : '';
$email  = isset($_POST['email'])  ? filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL) : '';
$consent = isset($_POST['consent']) ? ($_POST['consent'] === 'true' || $_POST['consent'] === '1') : false;

// --- Validation ---
if (empty($prenom) || mb_strlen($prenom) < 2) {
    echo json_encode(['status' => 'error', 'message' => 'Prenom requis (2 caracteres min).']);
    exit;
}
if (empty($nom) || mb_strlen($nom) < 2) {
    echo json_encode(['status' => 'error', 'message' => 'Nom requis (2 caracteres min).']);
    exit;
}
if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['status' => 'error', 'message' => 'Email invalide.']);
    exit;
}
if (!$consent) {
    echo json_encode(['status' => 'error', 'message' => 'Le consentement RGPD est obligatoire.']);
    exit;
}

// --- Load existing data ---
$db = load_db($db_file);

// --- Check duplicate email ---
foreach ($db as $entry) {
    if (isset($entry['email']) && strtolower($entry['email']) === strtolower($email)) {
        // Already registered -- success but no duplicate insert
        echo json_encode(['status' => 'success', 'message' => 'Deja inscrit.']);
        exit;
    }
}

// --- Build record ---
$record = [
    'id'          => uniqid('atelier_', true),
    'prenom'      => $prenom,
    'nom'         => $nom,
    'email'       => strtolower($email),
    'consent'     => true,
    'consent_at'  => date('Y-m-d H:i:s'),
    'created_at'  => date('Y-m-d H:i:s'),
    'brevo_synced' => false,
    'brevo_synced_at' => null,
];

$db[] = $record;

// --- Save ---
if (!save_db($db_file, $db_lock, $db)) {
    echo json_encode(['status' => 'error', 'message' => 'Erreur serveur (DB).']);
    exit;
}

// --- Sync Firestore (silencieux, ne bloque pas) ---
if (file_exists(__DIR__ . '/firestore.php')) {
    require_once __DIR__ . '/firestore.php';
    $fireId = firestore_add('atelier_inscriptions', $record);
    if ($fireId) {
        error_log("[KLEIA] Firestore OK: $fireId");
    }
}

// --- Email de confirmation (silencieux, ne bloque pas) ---
if (file_exists(__DIR__ . '/email-confirmation.php')) {
    require_once __DIR__ . '/email-confirmation.php';
    $emailResult = send_confirmation_email($prenom, $nom, $email);
    if ($emailResult['status'] === 'success') {
        error_log("[KLEIA] Email envoye a $email");
    } else {
        error_log("[KLEIA] Email ECHEC pour $email: " . $emailResult['message']);
    }
}

// --- Success ---
echo json_encode(['status' => 'success', 'message' => 'Inscription enregistree.']);
