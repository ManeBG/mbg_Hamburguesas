// src/utils/whats.js
import { normalizaTelefonoMX } from "./phone";

/**
 * Abre WhatsApp con un resumen formateado.
 * @param {{ to: string, pedidoId: number, nombre: string, telefono: string, items: any[], total: string|number, direccionEntrega: string }} p
 */
export function abrirWhatsResumen(p) {
  const mensaje = buildMensajeResumen(p);
  const url = `https://wa.me/${p.to}?text=${encodeURIComponent(mensaje)}`;

  // Intento abrir en nueva pestaña; si el navegador bloquea popups, hacemos fallback.
  const win = window.open(url, "_blank");
  if (!win) {
    window.location.href = url;
  }
}

/** Construye el texto que vas a enviar por Whats */
export function buildMensajeResumen({ pedidoId, nombre, telefono, items, total, direccionEntrega }) {
  const tel = normalizaTelefonoMX(telefono);
  const articulos = (items || [])
    .map(i => {
      const cant = i.cantidad || 1;
      const nombreProd = i.nombre_producto || i.nombre || "Producto";
      const subt = Number(i.subtotal ?? 0).toFixed(2);
      return `• ${cant} x ${nombreProd} ($${subt})`;
    })
    .join("\n");

  const totalStr = Number(total ?? 0).toFixed(2);

  return `
Pedido #${pedidoId}
Cliente: ${nombre} - ${tel}
Artículos:
${articulos}
Total: $${totalStr}
Entrega: ${direccionEntrega}`.trim();
}

/**
 * Devuelve el número E164 MX para WhatsApp: 52 + 10 dígitos
 * Si viene vacío, regresa null
 */
export function telefonoParaWhats(tel) {
  const n = normalizaTelefonoMX(tel);
  return n ? n : null;
}
