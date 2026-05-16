<?php
header('Content-Type: text/plain; charset=utf-8');
$db = __DIR__ . '/../data/atelier-inscriptions.json';
$lock = __DIR__ . '/../data/atelier-subscribe.lock';

if (!file_exists($db)) { echo "DB vide.\n"; exit; }

$fp = fopen($lock, 'c');
flock($fp, LOCK_EX);

$data = json_decode(file_get_contents($db), true);
$before = count($data);

// Garder uniquement jpp180866@gmail.com (le vrai)
$kept = [];
foreach ($data as $e) {
    if ($e['email'] === 'jpp180866@gmail.com') {
        $kept[] = $e;
    }
}
$after = count($kept);

file_put_contents($db, json_encode($kept, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
flock($fp, LOCK_UN);
fclose($fp);

echo "Nettoyage termine.\n";
echo "Avant : $before entrees\n";
echo "Apres : $after entrees\n";
