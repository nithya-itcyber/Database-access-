from datetime import date, timedelta
from decimal import Decimal
from db import get_connection


SOCIETES_FICTIVES = [
    ("Helios Volt SA", "HLSV", "Energie", "France", "EUR"),
    ("KronoMed Labo", "KMED", "Sante", "France", "EUR"),
    ("Nordic Rail Systems", "NDRS", "Industrie", "Suede", "SEK"),
    ("Vallee Numerique SAS", "VLNM", "Technologie", "France", "EUR"),
]

# (symbole, annee, ca, resultat_net, actifs_courants, passifs_courants, dettes_totales, capitaux_propres, total_actifs)
BILANS_FICTIFS = [
    # Helios Volt SA
    ("HLSV", 2023, "1200000.00", "96000.00", "420000.00", "210000.00", "350000.00", "700000.00", "1050000.00"),
    ("HLSV", 2024, "1450000.00", "130500.00", "490000.00", "245000.00", "380000.00", "820000.00", "1200000.00"),
    ("HLSV", 2025, "1700000.00", "170000.00", "560000.00", "280000.00", "400000.00", "960000.00", "1360000.00"),
    # KronoMed Labo
    ("KMED", 2023, "900000.00", "72000.00", "310000.00", "155000.00", "220000.00", "550000.00", "770000.00"),
    ("KMED", 2024, "1050000.00", "94500.00", "360000.00", "180000.00", "240000.00", "640000.00", "880000.00"),
    ("KMED", 2025, "1250000.00", "0.00", "400000.00", "0.00", "260000.00", "0.00", "950000.00"),
    # Nordic Rail Systems
    ("NDRS", 2023, "2100000.00", "147000.00", "680000.00", "340000.00", "510000.00", "1020000.00", "1530000.00"),
    ("NDRS", 2024, "2300000.00", "184000.00", "740000.00", "370000.00", "530000.00", "1150000.00", "1680000.00"),
    ("NDRS", 2025, "2500000.00", "225000.00", "810000.00", "405000.00", "550000.00", "1300000.00", "1850000.00"),
    # Vallee Numerique SAS
    ("VLNM", 2023, "750000.00", "60000.00", "290000.00", "145000.00", "180000.00", "450000.00", "630000.00"),
    ("VLNM", 2024, "880000.00", "79200.00", "330000.00", "165000.00", "195000.00", "520000.00", "715000.00"),
    ("VLNM", 2025, "1020000.00", "102000.00", "380000.00", "190000.00", "210000.00", "600000.00", "810000.00"),
]

COURS_BASE = {
    "HLSV": (Decimal("42.00"), Decimal("1.50"), 12000),
    "KMED": (Decimal("68.50"), Decimal("2.00"), 8500),
    "NDRS": (Decimal("115.00"), Decimal("-1.25"), 15000),
    "VLNM": (Decimal("31.00"), Decimal("1.10"), 9500),
}


def recharger() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cours")
            cur.execute("DELETE FROM bilan")
            cur.execute("DELETE FROM societe")

            symbole_to_id: dict[str, int] = {}
            for nom, symbole, secteur, pays, devise in SOCIETES_FICTIVES:
                cur.execute(
                    """
                    INSERT INTO societe (nom, symbole, secteur, pays, devise)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (nom, symbole, secteur, pays, devise),
                )
                symbole_to_id[symbole] = int(cur.lastrowid)

            for symbole, annee, ca, rn, ac, pc, dt, cp, ta in BILANS_FICTIFS:
                cur.execute(
                    """
                    INSERT INTO bilan (
                        societe_id, annee, chiffre_affaires, resultat_net,
                        actifs_courants, passifs_courants, dettes_totales,
                        capitaux_propres, total_actifs
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        symbole_to_id[symbole],
                        annee,
                        Decimal(ca),
                        Decimal(rn),
                        Decimal(ac),
                        Decimal(pc),
                        Decimal(dt),
                        Decimal(cp),
                        Decimal(ta),
                    ),
                )

            date_depart = date(2026, 11, 2)
            for symbole, societe_id in symbole_to_id.items():
                prix_initial, pas, volume_base = COURS_BASE[symbole]
                for jour_idx in range(10):
                    date_cours = date_depart + timedelta(days=jour_idx)
                    cours_cloture = prix_initial + (pas * Decimal(jour_idx))
                    volume = volume_base + (jour_idx * 250)
                    cur.execute(
                        """
                        INSERT INTO cours (societe_id, date_cours, cours_cloture, volume)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (societe_id, date_cours, cours_cloture, volume),
                    )

        conn.commit()
        print("Jeu de test rechargé : 4 sociétés, 12 bilans (3/société), 40 cours (10/société).")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    recharger()
