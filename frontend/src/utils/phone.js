// src/utils/phone.js

/** Limpia a dígitos y asume MX si son 10 dígitos. Devuelve "52XXXXXXXXXX" o "52..." si ya venía con 52 */
export function normalizaTelefonoMX(raw) {
  if (!raw) return null;
  const soloDigitos = String(raw).replace(/\D/g, "");
  if (soloDigitos.startsWith("52") && soloDigitos.length === 12) return soloDigitos;
  if (soloDigitos.length === 10) return "52" + soloDigitos;
  // Si no cuadra, igual devolvemos lo que haya por si es internacional
  return soloDigitos;
}
