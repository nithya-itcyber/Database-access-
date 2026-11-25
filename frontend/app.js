const SOCIETES = [
  { id: 1, nom: "Helios Volt SA", symbole: "HLSV", secteur: "Energie", pays: "France", devise: "EUR" },
  { id: 2, nom: "KronoMed Labo", symbole: "KMED", secteur: "Sante", pays: "France", devise: "EUR" },
  { id: 3, nom: "Nordic Rail Systems", symbole: "NDRS", secteur: "Industrie", pays: "Suede", devise: "SEK" },
  { id: 4, nom: "Vallee Numerique SAS", symbole: "VLNM", secteur: "Technologie", pays: "France", devise: "EUR" }
];

const container = document.getElementById("societes-list");
container.innerHTML = SOCIETES.map(
  (s) => `<p><strong>${s.nom}</strong> (${s.symbole}) - ${s.secteur} · ${s.pays} [${s.devise}]</p>`
).join("");
