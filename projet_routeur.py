import os
import re
from getpass import getpass
from netmiko import ConnectHandler

USER = os.getenv("ROUTEUR_USER") or input("Username : ")
PASS = os.getenv("ROUTEUR_PASS") or getpass("Mot de passe : ")

cisco1 = {
    "device_type": "cisco_xr",   # IOS XR (et non cisco_nxos)
    "host": "sandbox-iosxr-1.cisco.com",
    "username": USER,
    "password": PASS,
}


def parse_interfaces(sortie):
    interfaces = []
    motif = re.compile(
        r"^(\S+)\s+(\S+)\s+(administratively down|shutdown|up|down)\s+(up|down)",
        re.IGNORECASE,
    )
    for ligne in sortie.splitlines():
        m = motif.match(ligne.strip())
        if m:
            interfaces.append((m.group(1), m.group(2), m.group(3)))
    return interfaces


def main():
    print("Connexion au routeur...")
    with ConnectHandler(**cisco1) as conn:
        print("Connecté.")

        print("\n=== 1. Informations générales ===")
        run_cfg = conn.send_command("show running-config")
        version = conn.send_command("show version")

        m = re.search(r"^hostname\s+(\S+)", run_cfg, re.MULTILINE)
        print("Nom du routeur :", m.group(1) if m else conn.find_prompt())

        m = re.search(r"Version\s*:?\s*([\w\.\(\)]+)", version, re.IGNORECASE)
        print("Version OS     :", m.group(1) if m else "non trouvée")

        m = re.search(r"(cisco\s+[\w\s\-]+?)(?:\s+Series|\s+\(|\n)", version, re.IGNORECASE)
        print("Modèle         :", m.group(1).strip() if m else "non trouvé")

        brief = conn.send_command("show ip interface brief")
        interfaces = parse_interfaces(brief)

        print("\n=== 2. Interfaces UP ===")
        for nom, ip, statut in interfaces:
            if statut.lower() == "up":
                print(f"  {nom:<30} {ip}")

        print("\n=== 3. Interfaces DOWN ===")
        for nom, ip, statut in interfaces:
            if statut.lower() != "up":
                print(f"  {nom:<30} {ip}  ({statut})")

        print("\n=== 4. Nombre d'interfaces ===")
        nb_fast = sum(1 for n, _, _ in interfaces if n.lower().startswith("fastethernet"))
        nb_giga = sum(1 for n, _, _ in interfaces if n.lower().startswith("gigabitethernet"))
        print("  FastEthernet    :", nb_fast)
        print("  GigabitEthernet :", nb_giga)

        print("\n=== 5. Réseaux accessibles ===")
        routes = conn.send_command("show ip route")
        reseaux = []
        for ligne in routes.splitlines():
            m = re.search(r"(\d+\.\d+\.\d+\.\d+/\d+)", ligne)
            if m and m.group(1) not in reseaux:
                reseaux.append(m.group(1))
        for r in reseaux:
            print("  ", r)


if __name__ == "__main__":
    main()
