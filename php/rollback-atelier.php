<?php
/**
 * KLEIA-UP - Rollback Atelier
 * Permet de revenir en arriere si le popup pose probleme.
 * Usage (HTTP): php/rollback-atelier.php?token=kleia-bravo-2026
 * Usage (CLI):  php php/rollback-atelier.php backup
 *               php php/rollback-atelier.php restore
 *               php php/rollback-atelier.php status
 */

$token = isset($_GET['token']) ? $_GET['token'] : '';
$isHttp = (PHP_SAPI !== 'cli');

if ($isHttp && $token !== 'kleia-bravo-2026') {
    header('HTTP/1.1 403 Forbidden');
    echo "Access non autorise.";
    exit;
}

$backupDir = __DIR__ . '/../data/rollback';
$indexFile = __DIR__ . '/../index.html';
$backupFile = $backupDir . '/index-backup.html';

function log_msg($msg) {
    global $isHttp;
    echo ($isHttp ? ($msg . "<br>\n") : ($msg . "\n"));
    flush();
}

// Determine action
$action = 'status';
if ($isHttp) {
    $action = isset($_GET['action']) ? $_GET['action'] : 'status';
} else {
    $action = isset($argv[1]) ? $argv[1] : 'status';
}

// --- STATUS ---
if ($action === 'status') {
    $hasBackup = file_exists($backupFile);
    $popupActive = false;

    if (file_exists($indexFile)) {
        $content = file_get_contents($indexFile);
        $popupActive = (strpos($content, 'atelier-popup.js') !== false);
    }

    log_msg("=== STATUT POPUP ATELIER ===");
    log_msg("Backup existant  : " . ($hasBackup ? 'OUI' : 'NON'));
    log_msg("Popup actif      : " . ($popupActive ? 'OUI' : 'NON'));
    log_msg("PHP endpoint     : " . (file_exists(__DIR__ . '/atelier-subscribe.php') ? 'OK' : 'MANQUANT'));
    log_msg("Fichier popup JS : " . (file_exists(__DIR__ . '/../js/atelier-popup.js') ? 'OK' : 'MANQUANT'));
    log_msg("Page confirmation: " . (file_exists(__DIR__ . '/../atelier-place.html') ? 'OK' : 'MANQUANT'));
    log_msg("Sync Brevo       : " . (file_exists(__DIR__ . '/brevo-sync.php') ? 'OK' : 'MANQUANT'));
    exit;
}

// --- BACKUP ---
if ($action === 'backup') {
    if (!is_dir($backupDir)) {
        mkdir($backupDir, 0755, true);
    }

    if (!file_exists($indexFile)) {
        log_msg("ERREUR: index.html introuvable.");
        exit(1);
    }

    if (file_exists($backupFile)) {
        log_msg("AVERTISSEMENT: un backup existe deja. Utilisez 'restore' pour le restaurer, ou supprimez-le manuellement.");
        log_msg("Le backup actuel date de: " . date('Y-m-d H:i:s', filemtime($backupFile)));
        exit(1);
    }

    $original = file_get_contents($indexFile);
    if (file_put_contents($backupFile, $original)) {
        log_msg("BACKUP cree : " . $backupFile);
    } else {
        log_msg("ERREUR: impossible de creer le backup.");
        exit(1);
    }
    exit;
}

// --- RESTORE ---
if ($action === 'restore') {
    if (!file_exists($backupFile)) {
        log_msg("Aucun backup a restaurer.");
        exit(1);
    }

    // Backup l'etat actuel avant de restaurer (paranoia)
    if (file_exists($indexFile)) {
        $current = file_get_contents($indexFile);
        $snapshotFile = $backupDir . '/index-snapshot-' . date('Ymd_His') . '.html';
        file_put_contents($snapshotFile, $current);
        log_msg("Snapshot actuel sauvegarde: " . $snapshotFile);
    }

    $backupContent = file_get_contents($backupFile);
    if (file_put_contents($indexFile, $backupContent)) {
        unlink($backupFile); // Nettoyer le backup
        log_msg("RESTAURATION OK. index.html est revenu a l'etat sans popup.");
    } else {
        log_msg("ERREUR: restauration echouee.");
        exit(1);
    }
    exit;
}

// --- UNKNOWN ---
log_msg("Action inconnue: $action. Utilisez backup, restore, ou status.");
