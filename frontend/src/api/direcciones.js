// src/api/direcciones.js
export async function listarDirecciones(userId) {
  try {
    const r = await fetch(`/api/direcciones?user_id=${userId}`);
    const raw = await r.text();
    let data = null;
    try { data = raw ? JSON.parse(raw) : null; } catch {}
    if (!r.ok) return [];
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

export async function crearDireccion(payload) {
  try {
    const r = await fetch(`/api/direcciones`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const raw = await r.text();
    let data = null;
    try { data = raw ? JSON.parse(raw) : null; } catch {}
    if (!r.ok) return null;
    // esperamos { id } o { direccion_id }
    return data;
  } catch {
    return null;
  }
}
