<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    die('POST requis.');
}

$token = isset($_POST['token']) ? $_POST['token'] : '';
if ($token !== 'kleia-setup-2026') {
    http_response_code(403);
    die('Token invalide.');
}

$apiKey = isset($_POST['brevo_key']) ? trim($_POST['brevo_key']) : '';
if (empty($apiKey)) {
    die('Cle manquante.');
}

$listId = isset($_POST['brevo_list']) ? intval($_POST['brevo_list']) : 14;

$config = "<?php\nreturn [\n    'brevo_api_key' => '$apiKey',\n    'brevo_list_id' => $listId,\n];\n";
$written = file_put_contents(__DIR__ . '/config.php', $config);

if ($written) {
    // Auto-destruction
    unlink(__FILE__);
    echo "OK: config.php cree, install-config.php supprime.";
} else {
    echo "ERREUR: ecriture impossible.";
}
