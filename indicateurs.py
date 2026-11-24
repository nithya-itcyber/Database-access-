from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable


def _to_decimal_or_none(value: object) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        dec = value if isinstance(value, Decimal) else Decimal(str(value))
    except Exception:
        return None
    if not dec.is_finite():
        return None
    return dec


def _round_2(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def marge_nette(
    resultat_net: float | int | Decimal | None,
    chiffre_affaires: float | int | Decimal | None,
) -> float | None:
    """Return net margin in percent rounded to 2 decimals, or None if impossible."""
    rn = _to_decimal_or_none(resultat_net)
    ca = _to_decimal_or_none(chiffre_affaires)
    if rn is None or ca is None or ca == Decimal("0"):
        return None
    return _round_2((rn / ca) * Decimal("100"))


def liquidite(
    actifs_courants: float | int | Decimal | None,
    passifs_courants: float | int | Decimal | None,
) -> float | None:
    """Return current liquidity ratio rounded to 2 decimals, or None if impossible."""
    ac = _to_decimal_or_none(actifs_courants)
    pc = _to_decimal_or_none(passifs_courants)
    if ac is None or pc is None or pc == Decimal("0"):
        return None
    return _round_2(ac / pc)


def endettement(
    dettes_totales: float | int | Decimal | None,
    capitaux_propres: float | int | Decimal | None,
) -> float | None:
    """Return debt-to-equity ratio rounded to 2 decimals, or None if impossible."""
    dt = _to_decimal_or_none(dettes_totales)
    cp = _to_decimal_or_none(capitaux_propres)
    if dt is None or cp is None or cp == Decimal("0"):
        return None
    return _round_2(dt / cp)


def rendement(
    cours_debut: float | int | Decimal | None,
    cours_fin: float | int | Decimal | None,
) -> float | None:
    """Return percentage return between start and end price, or None if impossible."""
    debut = _to_decimal_or_none(cours_debut)
    fin = _to_decimal_or_none(cours_fin)
    if debut is None or fin is None or debut == Decimal("0"):
        return None
    return _round_2(((fin - debut) / debut) * Decimal("100"))


def moyenne_mobile(
    cours: Iterable[float | int | Decimal | None] | None,
    fenetre: int,
) -> list[float] | None:
    """Return moving average list over window `fenetre`, or None if invalid."""
    if cours is None or isinstance(fenetre, bool) or not isinstance(fenetre, int) or fenetre < 1:
        return None

    series: list[Decimal] = []
    for item in cours:
        parsed = _to_decimal_or_none(item)
        if parsed is None:
            return None
        series.append(parsed)

    if not series:
        return None

    result: list[float] = []
    for i in range(len(series)):
        start_idx = max(0, i - fenetre + 1)
        window_slice = series[start_idx : i + 1]
        avg = sum(window_slice, Decimal("0")) / Decimal(len(window_slice))
        result.append(_round_2(avg))

    return result
