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

// 2. Récupération et nettoyage des données
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $prenom = strip_tags(trim($_POST['prenom']));
    $nom = strip_tags(trim($_POST['nom']));
    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL);

    if (empty($prenom) || empty($nom) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['status' => 'error', 'message' => 'Données invalides.']);
        exit;
    }

    // 3. Construction du message
    $message = "Bonjour,\n\n";
    $message .= "Un nouveau prospect a valide le formulaire Entreprises :\n\n";
    $message .= "--------------------------------------------------\n";
    $message .= "Prenom : $prenom\n";
    $message .= "Nom    : $nom\n";
    $message .= "Email  : $email\n";
    $message .= "--------------------------------------------------\n\n";
    $message .= "L'utilisateur a ete redirige vers l'agenda Google.\n";

    // 4. En-têtes optimisés pour Gmail
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
