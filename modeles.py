from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Societe:
    nom: str
    symbole: str
    secteur: str
    pays: str
    devise: str = "EUR"
    id: int | None = None


@dataclass
class Bilan:
    societe_id: int
    annee: int
    chiffre_affaires: Decimal
    resultat_net: Decimal
    actifs_courants: Decimal
    passifs_courants: Decimal
    dettes_totales: Decimal
    capitaux_propres: Decimal
    total_actifs: Decimal
    id: int | None = None


@dataclass
class Cours:
    societe_id: int
    date_cours: date
    cours_cloture: Decimal
    volume: int
    id: int | None = None
