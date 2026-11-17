# Projet Netmiko : informations d'un routeur Cisco IOS XR

**Auteur :** TSHIMANGA BWENDE Japhet
**Formation / Classe :** M2 Devops, UDBL
**Cours / Enseignant :** DEVNET / PROF BLAISE ANGOMA
**Date :** 16 novembre 2026

Programme Python qui se connecte à un routeur avec Netmiko et affiche :
1. le nom, la version de l'OS et le modèle ;
2. les interfaces UP ;
3. les interfaces DOWN ;
4. le nombre d'interfaces FastEthernet et GigabitEthernet ;
5. les réseaux accessibles (show ip route).

## Installation
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Utilisation
    python3 projet_routeur.py

Le programme demande le username et le mot de passe. On peut aussi les fournir par variables d'environnement (ROUTEUR_USER et ROUTEUR_PASS).

Les identifiants sont personnels et temporaires : il faut réserver le sandbox Cisco DevNet « IOS XR Always-On » (devnetsandbox.cisco.com), puis copier le username et le password depuis la carte Access Details de la réservation.

## Remarque
Le sujet indique `device_type: cisco_nxos`, mais le routeur (`sandbox-iosxr-1`) tourne sous IOS XR. Le type Netmiko utilisé est donc `cisco_xr`.

Un exemple de résultat est dans `resultat.txt`.
