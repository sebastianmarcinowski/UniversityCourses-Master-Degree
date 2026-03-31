<?php

function oracle($cipherText, $method, $key, $iv) {
    $decrypted = openssl_decrypt($cipherText, $method, $key, OPENSSL_RAW_DATA | OPENSSL_ZERO_PADDING, $iv);
    $len = strlen($decrypted);
    if ($len === 0) return false;

    $padding = ord($decrypted[$len - 1]);
    if ($padding < 1 || $padding > 16) return false;

    for ($i = 0; $i < $padding; $i++) {
        if (ord($decrypted[$len - 1 - $i]) !== $padding) {
            return false;
        }
    }
    return true;
}

$method = "aes-128-cbc";
$key = random_bytes(16);
$iv = random_bytes(16);

echo "Podaj ciąg znaków do zaszyfrowania: ";
$userInput = rtrim(fgets(STDIN), "\r\n");
echo "Oryginalny tekst: " . $userInput . "\n";

$ciphertext = openssl_encrypt($userInput, $method, $key, OPENSSL_RAW_DATA, $iv);
echo "Szyfrogram (hex): " . bin2hex($ciphertext) . "\n";

$blocks = str_split($ciphertext, 16);

foreach ($blocks as $block) {
    echo "Block: " . $block . "\n";
}

$numBlocks = count($blocks);
$recoveredFull = "";

for ($i = 0; $i < $numBlocks; $i++) {
    $currentBlock = $blocks[$i];
    $previousBlock = ($i == 0) ? $iv : $blocks[$i - 1];

    $intermediary = str_repeat("\x00", 16);
    $decryptedBlock = str_repeat("\x00", 16);

    for ($byte = 15; $byte>=0; $byte--) {
        $expectedPadding = 16-$byte;

        for ($guessedValue = 0; $guessedValue < 256; $guessedValue++) {
            $testIv = str_repeat("\x00", $byte);
            $testIv .= chr($guessedValue);

            for ($k = $byte + 1; $k < 16; $k++) {
                $testIv .= chr(ord($intermediary[$k]) ^ $expectedPadding);
            }

            if (oracle($currentBlock, $method, $key, $testIv)) {
                $intermediary[$byte] = chr($guessedValue ^ $expectedPadding);
                $decryptedBlock[$byte] = chr(ord($intermediary[$byte]) ^ ord($previousBlock[$byte]));
                break;
            }
        }
    }
    echo "Odczytany blok " . ($i + 1) . ": [" . addcslashes($decryptedBlock, "\0..\37") . "]\n";
    if ($i > 0) {
        $recoveredFull .= $decryptedBlock;
    }
}

echo "\nOdzyskana wiadomość (bez pierwszego bloku): " . $recoveredFull . "\n";