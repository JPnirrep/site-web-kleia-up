<?php
header('Content-Type: text/plain; charset=utf-8');
$db = __DIR__ . '/../data/atelier-inscriptions.json';
if (!file_exists($db)) { die("Aucune DB.\n"); }

$data = json_decode(file_get_contents($db), true);
$before = count($data);

// Garder uniquement l'email reel
$kept = [];
foreach ($data as $e) {
    if ($e['email'] === 'jpp180866@gmail.com') {
        $kept[] = $e;
    }
}
file_put_contents($db, json_encode($kept, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
// Auto-destruction
unlink(__FILE__);
echo "OK: $before -> " . count($kept) . " entrees.\n";
