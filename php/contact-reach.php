<?php
/**
 * Script de traitement du formulaire de contact KLEIA-UP
 * Version : 1.0 - Option B (PHP Frugal)
 */

header('Content-Type: application/json; charset=utf-8');

// 1. Configuration - REMPLACE PAR TON EMAIL SI BESOIN
$to = "sandrina@kleia-up.fr, jpp180866@gmail.com"; 
$subject = "🚀 Nouveau Contact Entreprise - KLEIA-UP";

// 2. Récupération et nettoyage des données
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $prenom = strip_tags(trim($_POST['prenom']));
    $nom = strip_tags(trim($_POST['nom']));
    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL);

    // Vérification basique
    if (empty($prenom) || empty($nom) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['status' => 'error', 'message' => 'Données invalides.']);
        exit;
    }

    // 3. Construction du message
    $message = "Bonjour Sandrina,\n\n";
    $message .= "Un nouveau prospect vient de valider le formulaire sur la page Entreprises :\n\n";
    $message .= "--------------------------------------------------\n";
    $message .= "Prénom : $prenom\n";
    $message .= "Nom    : $nom\n";
    $message .= "Email  : $email\n";
    $message .= "--------------------------------------------------\n\n";
    $message .= "L'utilisateur a été redirigé vers ton agenda Google pour fixer un rendez-vous.\n";
    $message .= "\nCordialement,\nTon assistant KLEIA-UP Automatique.";

    // 4. En-têtes de l'email
    $headers = "From: Formulaire Site Web <noreply@kleia-up.fr>\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();

    // 5. Envoi
    if (mail($to, $subject, $message, $headers)) {
        echo json_encode(['status' => 'success', 'message' => 'Email envoyé avec succès.']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Erreur lors de l\'envoi de l\'email.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Méthode non autorisée.']);
}
?>
