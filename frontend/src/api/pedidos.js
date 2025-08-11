// src/api/pedidos.js
export async function crearPedido(payload) {
  try {
    const r = await fetch(`/api/pedidos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    // Lee como texto primero para poder loguear cualquier HTML/ vacío
    const raw = await r.text();

    let data = null;
    try { data = raw ? JSON.parse(raw) : null; } catch {
      // Si vino HTML/otro, deja data en null
    }

    if (!r.ok) {
      return {
        ok: false,
        status: r.status,
        error: (data && (data.error || data.message)) || raw || "Error HTTP"
      };
    }

    return { ok: true, status: r.status, data };
  } catch (e) {
    return { ok: false, status: 0, error: e.message || "Network error" };
  }
}
