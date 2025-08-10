// src/api/pedidos.js
export async function crearPedido(payload) {
  try {
    const r = await fetch("/api/pedidos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await r.json();
    if (!r.ok) return { ok: false, error: data.error || "Error al crear pedido" };
    // Esperamos algo como: { pedido_id, total, direccion_entrega, estado }
    return { ok: true, data };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}
