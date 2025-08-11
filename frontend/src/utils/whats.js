// src/utils/whats.js
import { normalizaTelefonoMX } from "./phone"

export function buildMensajeResumen({ pedidoId, nombre, telefono, items, total, direccionEntrega }) {
  const tel = normalizaTelefonoMX(telefono)
  const articulos = (items || [])
    .map(i => `• ${i.cantidad || 1} x ${i.nombre_producto || i.nombre || "Producto"} ($${Number(i.subtotal ?? 0).toFixed(2)})`)
    .join("\n")
  const totalStr = Number(total ?? 0).toFixed(2)
  return `
Pedido #${pedidoId}
Cliente: ${nombre} - ${tel}
Artículos:
${articulos}
Total: $${totalStr}
Entrega: ${direccionEntrega}`.trim()
}

export function abrirWhatsResumen(p) {
  const mensaje = buildMensajeResumen(p)
  const url = `https://wa.me/${p.to}?text=${encodeURIComponent(mensaje)}`
  const win = window.open(url, "_blank")
  if (!win) window.location.href = url
}

// Por si lo quieres importarlo así en Checkout.vue:
export function telefonoParaWhats(tel) {
  return normalizaTelefonoMX(tel)
}
