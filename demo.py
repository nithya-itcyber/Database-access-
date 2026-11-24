from db import get_connection
from depot import lister_bilans, lister_cours, lister_societes
from indicateurs import endettement, liquidite, marge_nette, moyenne_mobile, rendement


def _formater_valeur(valeur: float | None, suffixe: str = "") -> str:
    if valeur is None:
        return "Calcul impossible (donnée manquante ou division par zéro)"
    return f"{valeur}{suffixe}"


def executer_demo(symbole_cible: str = "HLSV", fenetre_mm: int = 3) -> None:
    conn = get_connection()
    try:
        societes = lister_societes(conn)
        if not societes:
            print("Aucune société trouvée dans la base.")
            return

        societe = next((s for s in societes if s.symbole == symbole_cible), societes[0])

        print("=== Informations de la société ===")
        print(f"ID       : {societe.id}")
        print(f"Nom      : {societe.nom}")
        print(f"Symbole  : {societe.symbole}")
        print(f"Secteur  : {societe.secteur}")
        print(f"Pays     : {societe.pays}")
        print(f"Devise   : {societe.devise}")

        bilans = lister_bilans(conn, societe.id)
        print("\n=== Indicateurs de la dernière année ===")
        if not bilans:
            print("Aucun bilan disponible pour cette société.")
        else:
            dernier_bilan = bilans[-1]
            print(f"Exercice : {dernier_bilan.annee}")
            print(
                "Marge nette    : "
                + _formater_valeur(
                    marge_nette(dernier_bilan.resultat_net, dernier_bilan.chiffre_affaires),
                    " %",
                )
            )
            print(
                "Liquidité      : "
                + _formater_valeur(
                    liquidite(dernier_bilan.actifs_courants, dernier_bilan.passifs_courants)
                )
            )
            print(
                "Endettement    : "
                + _formater_valeur(
                    endettement(dernier_bilan.dettes_totales, dernier_bilan.capitaux_propres)
                )
            )

        cours = lister_cours(conn, societe.id)
        print("\n=== Cours et moyenne mobile ===")
        if not cours:
            print("Aucun cours disponible pour cette société.")
        else:
            prix_cloture = [c.cours_cloture for c in cours]
            gain = rendement(prix_cloture[0], prix_cloture[-1])
            mm = moyenne_mobile(prix_cloture, fenetre_mm)
            print(
                f"Période        : {cours[0].date_cours} -> {cours[-1].date_cours} "
                f"({len(cours)} séances)"
            )
            print(
                f"Cours début/fin: {prix_cloture[0]} {societe.devise} -> "
                f"{prix_cloture[-1]} {societe.devise}"
            )
            print("Rendement      : " + _formater_valeur(gain, " %"))
            print(f"Moyenne mobile (fenêtre={fenetre_mm}) : {mm}")
    finally:
        conn.close()


if __name__ == "__main__":
    executer_demo()
