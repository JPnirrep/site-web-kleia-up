<?php
header('Content-Type: text/plain; charset=utf-8');
$db = __DIR__ . '/../data/atelier-inscriptions.json';
if (!file_exists($db)) { echo "Aucune entree."; exit; }
$data = json_decode(file_get_contents($db), true);
echo count($data) . " entree(s) :\n\n";
foreach ($data as $i => $e) {
    echo ($i+1) . ". {$e['prenom']} {$e['nom']} | {$e['email']} | RGPD: " . ($e['consent']?'oui':'non') . " | {$e['created_at']} | Brevo: " . ($e['brevo_synced']?'sync':'non') . "\n";
}
