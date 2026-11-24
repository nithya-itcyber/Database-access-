from datetime import date
from decimal import Decimal
import pymysql
from modeles import Bilan, Cours, Societe


def _to_decimal(value: object) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _row_to_societe(row: dict) -> Societe:
    return Societe(
        id=int(row["id"]),
        nom=str(row["nom"]),
        symbole=str(row["symbole"]),
        secteur=str(row["secteur"]),
        pays=str(row["pays"]),
    )


def _row_to_bilan(row: dict) -> Bilan:
    return Bilan(
        id=int(row["id"]),
        societe_id=int(row["societe_id"]),
        annee=int(row["annee"]),
        chiffre_affaires=_to_decimal(row["chiffre_affaires"]),
        resultat_net=_to_decimal(row["resultat_net"]),
        actifs_courants=_to_decimal(row["actifs_courants"]),
        passifs_courants=_to_decimal(row["passifs_courants"]),
        dettes_totales=_to_decimal(row["dettes_totales"]),
        capitaux_propres=_to_decimal(row["capitaux_propres"]),
        total_actifs=_to_decimal(row["total_actifs"]),
    )


def _row_to_cours(row: dict) -> Cours:
    raw_date = row["date_cours"]
    parsed_date = raw_date if isinstance(raw_date, date) else date.fromisoformat(str(raw_date))
    return Cours(
        id=int(row["id"]),
        societe_id=int(row["societe_id"]),
        date_cours=parsed_date,
        cours_cloture=_to_decimal(row["cours_cloture"]),
        volume=int(row["volume"]),
    )


def lister_societes(
    conn: pymysql.connections.Connection,
    secteur: str | None = None,
) -> list[Societe]:
    """Return companies as Societe objects, optionally filtered by secteur."""
    with conn.cursor() as cur:
        if secteur is not None and secteur != "":
            cur.execute(
                """
                SELECT id, nom, symbole, secteur, pays
                FROM societe
                WHERE secteur = %s
                ORDER BY nom ASC
                """,
                (secteur,),
            )
        else:
            cur.execute(
                """
                SELECT id, nom, symbole, secteur, pays
                FROM societe
                ORDER BY nom ASC
                """
            )
        rows = cur.fetchall()
    return [_row_to_societe(row) for row in rows]


def lire_societe(
    conn: pymysql.connections.Connection,
    societe_id: int,
) -> Societe | None:
    """Return a Societe by id, or None if not found."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, nom, symbole, secteur, pays
            FROM societe
            WHERE id = %s
            """,
            (societe_id,),
        )
        row = cur.fetchone()
    if row is None:
        return None
    return _row_to_societe(row)


def ajouter_societe(
    conn: pymysql.connections.Connection,
    societe: Societe,
) -> Societe:
    """Insert a Societe using parameters, commit on success, and rollback on error."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO societe (nom, symbole, secteur, pays)
                VALUES (%s, %s, %s, %s)
                """,
                (societe.nom, societe.symbole, societe.secteur, societe.pays),
            )
            new_id = cur.lastrowid
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return Societe(
        id=int(new_id) if new_id is not None else societe.id,
        nom=societe.nom,
        symbole=societe.symbole,
        secteur=societe.secteur,
        pays=societe.pays,
    )


def lister_bilans(
    conn: pymysql.connections.Connection,
    societe_id: int,
) -> list[Bilan]:
    """Return balance sheets for a company ordered by year ascending."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, societe_id, annee, chiffre_affaires, resultat_net,
                   actifs_courants, passifs_courants, dettes_totales,
                   capitaux_propres, total_actifs
            FROM bilan
            WHERE societe_id = %s
            ORDER BY annee ASC
            """,
            (societe_id,),
        )
        rows = cur.fetchall()
    return [_row_to_bilan(row) for row in rows]


def lister_cours(
    conn: pymysql.connections.Connection,
    societe_id: int,
    date_debut: date | None = None,
    date_fin: date | None = None,
) -> list[Cours]:
    """Return stock quotes for a company over an optional date range."""
    with conn.cursor() as cur:
        if date_debut is not None and date_fin is not None:
            cur.execute(
                """
                SELECT id, societe_id, date_cours, cours_cloture, volume
                FROM cours
                WHERE societe_id = %s
                  AND date_cours BETWEEN %s AND %s
                ORDER BY date_cours ASC
                """,
                (societe_id, date_debut, date_fin),
            )
        elif date_debut is not None:
            cur.execute(
                """
                SELECT id, societe_id, date_cours, cours_cloture, volume
                FROM cours
                WHERE societe_id = %s
                  AND date_cours >= %s
                ORDER BY date_cours ASC
                """,
                (societe_id, date_debut),
            )
        elif date_fin is not None:
            cur.execute(
                """
                SELECT id, societe_id, date_cours, cours_cloture, volume
                FROM cours
                WHERE societe_id = %s
                  AND date_cours <= %s
                ORDER BY date_cours ASC
                """,
                (societe_id, date_fin),
            )
        else:
            cur.execute(
                """
                SELECT id, societe_id, date_cours, cours_cloture, volume
                FROM cours
                WHERE societe_id = %s
                ORDER BY date_cours ASC
                """,
                (societe_id,),
            )
        rows = cur.fetchall()
    return [_row_to_cours(row) for row in rows]
