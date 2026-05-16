<?php
/**
 * KLEIA-UP - Email de confirmation atelier
 * Format texte brut (identique a contact-reach.php, prouve fonctionnel).
 * From: noreply@kleia-up.fr | Reply-To: sandrina@kleia-up.fr
 */

function send_confirmation_email($prenom, $nom, $email) {

    // Majuscule forcee sur le prenom
    if (function_exists('mb_strtoupper')) {
        $prenom = mb_strtoupper(mb_substr($prenom, 0, 1)) . mb_strtolower(mb_substr($prenom, 1));
    } else {
        $prenom = strtoupper(substr($prenom, 0, 1)) . strtolower(substr($prenom, 1));
    }

    $message = "Bonjour $prenom,\n\n";
    $message .= "Merci de t'etre inscrit(e) a l'atelier.\n\n";
    $message .= "<< Prendre sa place sans forcer >>\n\n";
    $message .= "Ce que nous allons vivre : c'est exactement ce que nous allons\n";
    $message .= "vivre ensemble mardi prochain.\n\n";
    $message .= "--------------------------------------------------\n";
    $message .= "Mardi 2 juin 2026\n";
    $message .= "12h00 - 13h00 (heure de Paris)\n";
    $message .= "En visio Google Meet\n";
    $message .= "--------------------------------------------------\n\n";
    $message .= "Lien : https://meet.google.com/wbz-emxy-udw\n";
    $message .= "Tel  : +33 1 87 40 02 06\n";
    $message .= "Code : 996 704 367#\n\n";
    $message .= "D'ici la, respire. Ta place t'attend deja.\n\n";
    $message .= "A mardi,\n";
    $message .= "Sandrina\n";
    $message .= "--\n";
    $message .= "KLEIA-UP";

    // Structure CONFORME a contact-reach.php (prouve 16/05)
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

    $sent = mail($to, $subject, $message, $headers, "-f$from");
    return $sent ? ['status' => 'success', 'message' => 'Email envoye.'] : ['status' => 'error', 'message' => 'Echec envoi mail().'];
}
