<?php
/**
 * Script de traitement du formulaire de contact KLEIA-UP
 * Version : 1.1 - Optimisation Délivrabilité Gmail
 */

header('Content-Type: application/json; charset=utf-8');

// 1. Configuration
$to = "sandrina@kleia-up.fr, jpp180866@gmail.com"; 
$subject = "=?UTF-8?B?".base64_encode("🚀 Nouveau Contact Entreprise - KLEIA-UP")."?=";
$from = "noreply@kleia-up.fr";
$cns_endpoint = "http://bot.antigravity-brain.com/leads"; // Central CNS Endpoint (Firebase Hub)

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
    // On pousse vers le Cerveau Central même avant l'envoi de l'email.
    $lead_payload = [
        "member_id" => "ANTIGRAVITY-CNS-KLEIA-UP",
        "name" => $nom_complet,
        "email" => $email,
        "subject" => $subject_form,
        "message" => $message_user,
        "metadata" => [
            "ip" => $_SERVER['REMOTE_ADDR'],
            "origin" => "Website KLEIA-UP",
            "device" => $_SERVER['HTTP_USER_AGENT']
        ]
    ];

    $ch = curl_init($cns_endpoint);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($lead_payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 3); // Ne bloque pas si le CNS est hors-ligne
    $cns_push = curl_exec($ch);
    curl_close($ch);

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
    $headers = "From: KLEIA-UP <$from>\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
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
