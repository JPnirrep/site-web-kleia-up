<?php
require_once __DIR__ . '/email-confirmation.php';
$result = send_confirmation_email('DirectTest', 'Final', 'jpp180866+final@gmail.com');
echo json_encode($result);
