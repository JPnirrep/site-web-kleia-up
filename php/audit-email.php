<?php
header('Content-Type: text/plain; charset=utf-8');

echo "=== AUDIT EMAIL KLEIA-UP ===\n\n";

// 1. Verifier que le fichier email-confirmation existe
echo "1. Fichier email-confirmation.php : " . (file_exists(__DIR__ . '/email-confirmation.php') ? "OK" : "MANQUANT") . "\n";
echo "   Taille : " . filesize(__DIR__ . '/email-confirmation.php') . " octets\n\n";

// 2. Tester mail() direct vers Gmail (sans + dans l'adresse)
$testEmail = "jpp180866@gmail.com";
$from = "noreply@kleia-up.fr";
$subject = "=?UTF-8?B?" . base64_encode("TEST AUDIT EMAIL") . "?=";
$msg = "Test audit direct mail() - " . date('H:i:s');
$msg_id = "<audit-" . time() . "@kleia-up.fr>";
$headers = "From: KLEIA-UP <$from>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Message-ID: $msg_id\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

$result = mail($testEmail, $subject, $msg, $headers, "-f$from");
echo "2. Test mail() direct vers $testEmail : " . ($result ? "OK (mail()=true)" : "KO (mail()=false)") . "\n";
echo "   php_uname: " . php_uname() . "\n";
echo "   PHP version: " . phpversion() . "\n";
echo "   sendmail_path: " . (ini_get('sendmail_path') ?: 'non defini') . "\n\n";

// 3. Tester avec contact-reach (meme structure)
$to = "sandrina@kleia-up.fr, jpp180866@gmail.com";
$subject2 = "=?UTF-8?B?" . base64_encode("TEST AUDIT contact-reach") . "?=";
$msg2 = "Audit : test via contact-reach pattern - " . date('H:i:s');
$msg_id2 = "<audit-cr-" . time() . "@kleia-up.fr>";
$headers2 = "From: KLEIA-UP <$from>\r\n";
$headers2 .= "MIME-Version: 1.0\r\n";
$headers2 .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers2 .= "Message-ID: $msg_id2\r\n";
$headers2 .= "X-Mailer: PHP/" . phpversion();

$result2 = mail($to, $subject2, $msg2, $headers2, "-f$from");
echo "3. Test contact-reach pattern : " . ($result2 ? "OK" : "KO") . "\n\n";

// 4. Tester l'email de confirmation directement
require_once __DIR__ . '/email-confirmation.php';
$result3 = send_confirmation_email('Audit', 'Test', 'jpp180866@gmail.com');
echo "4. Test send_confirmation_email() : " . $result3['status'] . " - " . $result3['message'] . "\n";

echo "\n=== FIN AUDIT ===";
