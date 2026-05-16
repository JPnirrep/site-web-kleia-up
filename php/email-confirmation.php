<?php
/**
 * KLEIA-UP - Email de confirmation atelier
 * CONTACT-REACH CONFORME - text/plain d'abord, HTML si confirme.
 */

function send_confirmation_email($prenom, $nom, $email) {

    if (function_exists('mb_strtoupper')) {
        $prenom = mb_strtoupper(mb_substr($prenom, 0, 1)) . mb_strtolower(mb_substr($prenom, 1));
    } else {
        $prenom = strtoupper(substr($prenom, 0, 1)) . strtolower(substr($prenom, 1));
    }

    $meetLink = 'https://meet.google.com/wbz-emxy-udw';
    $phoneNumber = '+33 1 87 40 02 06';
    $phoneCode = '996 704 367#';

    // Message EN CLAIR (comme contact-reach.php)
    $msg = "";
    $msg .= "Bonjour $prenom,\n\n";
    $msg .= "Merci de t'etre inscrit(e) a l'atelier.\n\n";
    $msg .= "<< Prendre sa place sans forcer >>\n\n";
    $msg .= "-- Mardi 2 juin 2026\n";
    $msg .= "-- 12h00 - 13h00 (Paris)\n";
    $msg .= "-- En visio Google Meet\n\n";
    $msg .= "LIEN : $meetLink\n";
    $msg .= "TEL : $phoneNumber - CODE : $phoneCode\n\n";
    $msg .= "D'ici la, respire. Ta place t'attend deja.\n\n";
    $msg .= "A mardi,\n";
    $msg .= "Sandrina\n";
    $msg .= "--\nKLEIA-UP";

    // EXACT contact-reach.php pattern (prouve 16/05)
    $to = "sandrina@kleia-up.fr, " . $email;
    $from = "noreply@kleia-up.fr";
    $subject = "=?UTF-8?B?" . base64_encode("Bienvenue - Atelier Prendre sa place sans forcer") . "?=";
    $msg_id = "<" . time() . "-" . md5($email) . "@kleia-up.fr>";

    $headers = "From: KLEIA-UP <$from>\r\n";
    $headers .= "Reply-To: sandrina@kleia-up.fr\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $headers .= "Message-ID: $msg_id\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    $sent = mail($to, $subject, $msg, $headers, "-f$from");
    return $sent ? ['status' => 'success', 'message' => 'Email envoye.'] : ['status' => 'error', 'message' => 'Echec envoi mail().'];
}
