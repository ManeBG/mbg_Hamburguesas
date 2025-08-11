// src/utils/whats.js
import { normalizaTelefonoMX } from "./phone"


export function armarTextoPedido({ pedidoId, nombre, telefono, items, total, direccionEntrega }) {
  const lineas = [];
  lineas.push(`Pedido #${pedidoId}`);
  lineas.push(`Cliente: ${nombre} - ${telefono.startsWith('+') ? telefono : '52' + telefono}`);
  lineas.push(`Artículos:`);

  for (const it of (items || [])) {
    const precio = Number(it.subtotal || 0).toFixed(2);
    lineas.push(`* ${it.cantidad || 1} x ${it.nombre_producto} ($${precio})`);
    if (it.toppings?.length) lineas.push(`   · + ${it.toppings.join(', ')}`);
    if (it.sin_ingredientes?.length) lineas.push(`   · - ${it.sin_ingredientes.join(', ')}`);
  }

  lineas.push(`Total: $${Number(total || 0).toFixed(2)}`);
  if (direccionEntrega) lineas.push(`Entrega: ${direccionEntrega}`);

  return lineas.join('\n');
}

// export function buildMensajeResumen({ pedidoId, nombre, telefono, items, total, direccionEntrega }) {
//   const tel = normalizaTelefonoMX(telefono)
//   const articulos = (items || [])
//     .map(i => `• ${i.cantidad || 1} x ${i.nombre_producto || i.nombre || "Producto"} ($${Number(i.subtotal ?? 0).toFixed(2)})`)
//     .join("\n")
//   const totalStr = Number(total ?? 0).toFixed(2)
//   return `
// Pedido #${pedidoId}
// Cliente: ${nombre} - ${tel}
// Artículos:
// ${articulos}
// Total: $${totalStr}
// Entrega: ${direccionEntrega}`.trim()
// }

export function abrirWhatsResumen(args) {
  const texto = armarTextoPedido(args);
  const to = args.to?.replace(/\D/g, '');
  if (!to) return;
  const url = `https://wa.me/${to}?text=${encodeURIComponent(texto)}`;
  window.open(url, '_blank');
}

// Por si lo quieres importarlo así en Checkout.vue:
export function telefonoParaWhats(tel) {
  return normalizaTelefonoMX(tel)
}
