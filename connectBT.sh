#!/bin/bash

# Adresse MAC de ton module Bluetooth
MAC="98:D3:71:FD:AC:FC"

echo "🔧 Configuration du profil série Bluetooth (SPP)..."
sudo sdptool add SP

echo "🔌 Libération des anciens ports rfcomm..."
sudo rfcomm release all

echo "🔗 Liaison avec le périphérique Bluetooth $MAC..."
sudo rfcomm bind /dev/rfcomm0 $MAC

echo "⏳ Vérification de la liaison..."
if [ -e /dev/rfcomm0 ]; then
    echo "✅ Port série /dev/rfcomm0 prêt à l'utilisation."
else
    echo "❌ Échec : /dev/rfcomm0 non disponible."
    echo "ℹ️ Vérifie que le périphérique est appairé et sous tension."
fi

