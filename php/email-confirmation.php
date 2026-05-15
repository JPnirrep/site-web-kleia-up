<?php
/**
 * KLEIA-UP - Email de confirmation atelier
 * Envoi via mail() PHP natif (From: sandrina@kleia-up.fr).
 * Appele par atelier-subscribe.php apres inscription.
 */

function send_confirmation_email($prenom, $nom, $email) {

    // Force majuscule sur le prenom (fallback si mbstring absent)
    if (function_exists('mb_strtoupper')) {
        $prenom = mb_strtoupper(mb_substr($prenom, 0, 1)) . mb_strtolower(mb_substr($prenom, 1));
    } else {
        $prenom = strtoupper(substr($prenom, 0, 1)) . strtolower(substr($prenom, 1));
    }

    $meetLink = 'https://meet.google.com/wbz-emxy-udw';
    $phoneNumber = '+33 1 87 40 02 06';
    $phoneCode = '996 704 367#';

    $html = '<!DOCTYPE html><html><body style="font-family:Georgia,serif;background:#FDFCF0;padding:30px">';
    $html .= '<div style="max-width:560px;margin:0 auto;background:#FFF;border-radius:20px;padding:35px;border:1px solid rgba(139,29,61,0.06)">';

    // Logo
    $html .= '<div style="text-align:center;margin-bottom:25px">';
    $html .= '<img src="https://kleia-up.fr/assets/logo_kleia.png" height="60" alt="KLEIA-UP">';
    $html .= '</div>';

    // Salutation
    $html .= '<p style="font-size:1.1rem;color:#1A1A1A;margin-bottom:15px">Bonjour ' . htmlspecialchars($prenom) . ',</p>';
    $html .= '<p style="font-size:0.95rem;color:#333;line-height:1.6;margin-bottom:20px">';
    $html .= 'Merci de t\'&ecirc;tre inscrit(e) &agrave; l\'atelier.</p>';

    // Citation
    $html .= '<p style="font-size:1.1rem;color:#8B1D3D;font-style:italic;line-height:1.6;margin-bottom:25px;text-align:center;font-weight:700">';
    $html .= '&laquo; Prendre sa place sans forcer &raquo; &mdash; c\'est exactement ce que nous allons vivre ensemble mardi prochain.</p>';

    // Infos
    $html .= '<div style="background:rgba(139,29,61,0.03);border-radius:15px;padding:20px;margin-bottom:25px">';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:8px">&#128197; <strong>Mardi 2 juin 2026</strong></p>';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:8px">&#128340; <strong>12h00 &ndash; 13h00</strong> (heure de Paris)</p>';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:15px">&#128205; En visio Google Meet</p>';

    // Bouton Meet
    $html .= '<div style="text-align:center;margin-bottom:15px">';
    $html .= '<a href="' . $meetLink . '" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#8B1D3D 0%,#D70040 100%);color:#FFF;padding:14px 28px;border-radius:12px;text-decoration:none;font-weight:800;font-size:1rem;text-transform:uppercase">Rejoindre la visio</a>';
    $html .= '</div>';

    // Telephone
    $html .= '<p style="font-size:0.82rem;color:#666;text-align:center;margin-bottom:3px">';
    $html .= 'Ou par t&eacute;l&eacute;phone : ' . $phoneNumber . ' &mdash; CODE : ' . $phoneCode;
    $html .= '</p>';
    $html .= '</div>';

    // Mot de fin
    $html .= '<p style="font-size:0.95rem;color:#333;line-height:1.6;margin-bottom:25px">';
    $html .= 'D\'ici l&agrave;, respire. Ta place t\'attend d&eacute;j&agrave;.</p>';

    // Signature
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:0">&Agrave; mardi,</p>';
    $html .= '<p style="font-size:1rem;color:#8B1D3D;font-weight:800;margin-bottom:15px">Sandrina</p>';

    $html .= '<hr style="border:none;border-top:1px solid rgba(139,29,61,0.1);margin:15px 0">';
    $html .= '<p style="font-size:0.75rem;color:#999">KLEIA-UP</p>';

    $html .= '</div></body></html>';

    // Envoi via mail() PHP natif (From: sandrina@kleia-up.fr sans proxy Brevo)
    $from = 'sandrina@kleia-up.fr';
    $fromName = 'Sandrina Perrin - KLEIA-UP';
    $subject = 'Bienvenue — Atelier « Prendre sa place sans forcer »';

    $headers  = "From: $fromName <$from>\r\n";
    $headers .= "Reply-To: $from\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "Message-ID: <atelier-" . time() . "-" . substr(md5($email), 0, 8) . "@kleia-up.fr>\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

    $sent = mail($email, $subject, $html, $headers, "-f$from");

    if ($sent) {
        return ['status' => 'success', 'message' => 'Email envoye.'];
    }
    return ['status' => 'error', 'message' => 'Echec envoi mail().'];
}
