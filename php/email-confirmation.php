<?php
/**
 * KLEIA-UP - Email de confirmation atelier
 * Envoi exactement comme contact-reach.php (prouve 16/05 vers Gmail).
 * From: noreply@kleia-up.fr | Reply-To: sandrina@kleia-up.fr
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

    $html = '<!DOCTYPE html><html><body style="font-family:Georgia,serif;background:#FDFCF0;padding:30px">';
    $html .= '<div style="max-width:560px;margin:0 auto;background:#FFF;border-radius:20px;padding:35px;border:1px solid rgba(139,29,61,0.06)">';
    $html .= '<div style="text-align:center;margin-bottom:25px"><img src="https://kleia-up.fr/assets/logo_kleia.png" height="60" alt="KLEIA-UP"></div>';
    $html .= '<p style="font-size:1.1rem;color:#1A1A1A;margin-bottom:15px">Bonjour ' . htmlspecialchars($prenom) . ',</p>';
    $html .= '<p style="font-size:0.95rem;color:#333;line-height:1.6;margin-bottom:20px">Merci de t\'&ecirc;tre inscrit(e) &agrave; l\'atelier.</p>';
    $html .= '<p style="font-size:1.1rem;color:#8B1D3D;font-style:italic;line-height:1.6;margin-bottom:25px;text-align:center;font-weight:700">&laquo; Prendre sa place sans forcer &raquo; &mdash; c\'est exactement ce que nous allons vivre ensemble mardi prochain.</p>';
    $html .= '<div style="background:rgba(139,29,61,0.03);border-radius:15px;padding:20px;margin-bottom:25px">';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:8px">&#128197; <strong>Mardi 2 juin 2026</strong></p>';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:8px">&#128340; <strong>12h00 &ndash; 13h00</strong> (heure de Paris)</p>';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:15px">&#128205; En visio Google Meet</p>';
    $html .= '<div style="text-align:center;margin-bottom:15px"><a href="' . $meetLink . '" target="_blank" style="display:inline-block;background:linear-gradient(135deg,#8B1D3D 0%,#D70040 100%);color:#FFF;padding:14px 28px;border-radius:12px;text-decoration:none;font-weight:800;font-size:1rem;text-transform:uppercase">Rejoindre la visio</a></div>';
    $html .= '<p style="font-size:0.82rem;color:#666;text-align:center;margin-bottom:3px">Ou par t&eacute;l&eacute;phone : ' . $phoneNumber . ' &mdash; CODE : ' . $phoneCode . '</p></div>';
    $html .= '<p style="font-size:0.95rem;color:#333;line-height:1.6;margin-bottom:25px">D\'ici l&agrave;, respire. Ta place t\'attend d&eacute;j&agrave;.</p>';
    $html .= '<p style="font-size:0.95rem;color:#1A1A1A;margin-bottom:0">&Agrave; mardi,</p>';
    $html .= '<p style="font-size:1rem;color:#8B1D3D;font-weight:800;margin-bottom:15px">Sandrina</p>';
    $html .= '<hr style="border:none;border-top:1px solid rgba(139,29,61,0.1);margin:15px 0">';
    $html .= '<p style="font-size:0.75rem;color:#999">KLEIA-UP</p>';
    $html .= '</div></body></html>';

    // EXACTEMENT comme contact-reach.php (prouve 16/05)
    $to = "sandrina@kleia-up.fr, " . $email;
    $from = "noreply@kleia-up.fr";
    $subject = "=?UTF-8?B?" . base64_encode("Bienvenue - Atelier Prendre sa place sans forcer") . "?=";
    $msg_id = "<" . time() . "-" . md5($email) . "@kleia-up.fr>";

    $headers = "From: KLEIA-UP <$from>\r\n";
    $headers .= "Reply-To: sandrina@kleia-up.fr\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "Message-ID: $msg_id\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    $sent = mail($to, $subject, $html, $headers, "-f$from");
    return $sent ? ['status' => 'success', 'message' => 'Email envoye.'] : ['status' => 'error', 'message' => 'Echec envoi mail().'];
}
