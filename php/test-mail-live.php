<?php
$to = "jpp180866+debug2@gmail.com";
$from = "noreply@kleia-up.fr";
$subject = "TEST DIRECT";
$msg = "Test via file";
$headers = "From: KLEIA-UP <$from>\r\n";
echo mail($to, $subject, $msg, $headers, "-f$from") ? "OK" : "KO";
