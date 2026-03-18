<?php
/**
 * Script de test simple pour vérifier la délivrabilité d'Hostinger vers Gmail.
 * Usage : Visitez http://kleia-up.fr/php/test-mail.php dans votre navigateur.
 */

$to = "jpp180866@gmail.com"; 
$from = "noreply@kleia-up.fr";
$subject = "🧪 TEST DÉLIVRABILITÉ - KLEIA-UP";

$headers = "From: KLEIA-UP <$from>\r\n";
$headers .= "Reply-To: $from\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$message = "Date de l'envoi : " . date('d/m/Y H:i:s') . "\n";
$message .= "Si tu reçois cet email, la connexion Hostinger -> Gmail fonctionne.\n";
$message .= "Sinon, vérifie tes SPAMS ou ajoute kleia-up.fr aux expéditeurs autorisés.\n";

echo "<h1>Lancement du test d'envoi...</h1>";
echo "Destinataire : $to<br>";
echo "Expéditeur : $from<br><br>";

if (mail($to, $subject, $message, $headers, "-f$from")) {
    echo "<span style='color: green; font-weight: bold;'>SUCCESS ! L'email a été accepté par le serveur de mail d'Hostinger.</span><br>";
    echo "Patience... cela peut prendre quelques minutes pour arriver chez Gmail.";
} else {
    echo "<span style='color: red; font-weight: bold;'>ERREUR FATALE : Le serveur mail d'Hostinger a refusé l'envoi.</span><br>";
    echo "Possible cause : L'adresse $from n'existe pas ou n'est pas autorisée sur cet hébergement.";
}
?>
