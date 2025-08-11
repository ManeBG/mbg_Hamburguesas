// src/utils/phone.js

export function normalizaTelefonoMX(raw) {
  if (!raw) return null
  const d = String(raw).replace(/\D/g, "")
  if (d.startsWith("52") && d.length === 12) return d
  if (d.length === 10) return "52" + d
  return d
}
