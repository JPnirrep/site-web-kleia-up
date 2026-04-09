<?php
/**
 * Script de traitement du formulaire de contact KLEIA-UP
 * Version : 1.1 - Optimisation Délivrabilité Gmail
 */

header('Content-Type: application/json; charset=utf-8');

// 1. Configuration Vagus OS (V8.3.3)
$cns_endpoint = "http://135.125.53.215:8001/capture"; 
$to = "sandrina@kleia-up.fr, jpp180866@gmail.com"; 
$subject = "=?UTF-8?B?".base64_encode("🚀 Une nouvelle personne vient de s'inscrire au challenge de Pâques")."?=";
$from = "noreply@kleia-up.fr";

/**
 * Fonction de Push CNS (Central Nervous System)
 * Avec détection de connectivité pour éviter de bloquer le script
 */
function push_to_cns($url, $payload) {
    if (!$url) return false;
    
    // Vérification rapide de la résolution DNS pour éviter le hang
    $host = parse_url($url, PHP_URL_HOST);
    if (gethostbyname($host) === $host) {
        // Le domaine ne résout pas encore (pas configuré)
        return false;
    }

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 2); 
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
    $result = @curl_exec($ch);
    return $result;
}

// 2. Récupération et nettoyage des données
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Mapping souple (Supporte 'name' de contact.html et 'prenom/nom' de entreprises.html)
    $prenom = isset($_POST['prenom']) ? strip_tags(trim($_POST['prenom'])) : '';
    $nom = isset($_POST['nom']) ? strip_tags(trim($_POST['nom'])) : '';
    $nom_complet = isset($_POST['name']) ? strip_tags(trim($_POST['name'])) : "$prenom $nom";

    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL);
    $subject_form = isset($_POST['subject']) ? strip_tags(trim($_POST['subject'])) : 'Mouvement / Journal';
    $message_user = isset($_POST['message']) ? strip_tags(trim($_POST['message'])) : 'Inscription au mouvement (Newsletter)';

    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['status' => 'error', 'message' => 'Email invalide.']);
        exit;
    }

    // --- CNS SYNC (Souveraineté & Mémoire Permanente) ---
    $lead_payload = [
        "member_id" => "ANTIGRAVITY-CNS-KLEIA-UP",
        "name" => $nom_complet,
        "email" => $email,
        "subject" => $subject_form,
        "message" => $message_user,
        "metadata" => [
            "ip" => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            "origin" => "Website KLEIA-UP",
            "device" => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
        ]
    ];

    push_to_cns($cns_endpoint, $lead_payload);

    // 3. Construction du message (Format Clair et Holistique)
    $message = "Bonjour,\n\n";
    $message .= "Une nouvelle interaction a eu lieu sur KLEIA-UP :\n\n";
    $message .= "--------------------------------------------------\n";
    $message .= "Type : $subject_form\n";
    $message .= "Nom  : $nom_complet\n";
    $message .= "Email : $email\n";
    $message .= "--------------------------------------------------\n\n";
    $message .= "Message/Infos :\n$message_user\n\n";
    $message .= "--------------------------------------------------\n";
    $message .= "L'utilisateur a été notifié de la réception du message.\n";

    // 4. En-têtes optimisés pour Gmail et Souveraineté
    // Ajout d'un identifiant de message unique pour Gmail
    $msg_id = "<" . time() . "-" . md5($email) . "@kleia-up.fr>";
    
    $headers = "From: KLEIA-UP <$from>\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $headers .= "Message-ID: $msg_id\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    // 5. Envoi avec paramètre d'enveloppe (-f) pour éviter le spam
    if (mail($to, $subject, $message, $headers, "-f$from")) {
        echo json_encode(['status' => 'success', 'message' => 'Email envoyé.']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Erreur technique d\'envoi.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Méthode non autorisée.']);
}
?>
