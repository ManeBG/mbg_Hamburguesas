<script setup>
import { ref, computed, onMounted } from "vue";
import { crearPedido } from "@/api/pedidos";
import { listarDirecciones, crearDireccion } from "@/api/direcciones";
import { abrirWhatsResumen, telefonoParaWhats } from "@/utils/whats";
import { carrito } from "@/store";

const form = ref({ nombre: "", telefono: "" });
const userId = ref(localStorage.getItem("user_id") || null);

const carritoItems = carrito;
const totalCarrito = computed(() => carritoItems.value.reduce((a, i) => a + Number(i.total || 0), 0));
const dataPedido = ref(null);
const abrirWhatsAuto = ref(true);
const NEGOCIO_TEL = import.meta.env.VITE_NEGOCIO_TEL;

// ---- Direcciones ----
const direcciones = ref([]);          // lista del backend
const seleccion = ref("");            // "id:10" | "nueva" | "" | "texto"
const nueva = ref({ calle:"", colonia:"", ciudad:"", referencias:"", guardar:true });
const direccionTexto = ref("");       // textarea cuando no hay sesión o elige "texto"

// carga direcciones si hay user
onMounted(async () => {
  // autocompleta nombre/tel si traes guardado
  const nombreLS = localStorage.getItem("nombre"); 
  const telLS = localStorage.getItem("telefono");
  if (nombreLS) form.value.nombre = nombreLS;
  if (telLS) form.value.telefono = telLS;

  if (userId.value) {
    direcciones.value = await listarDirecciones(userId.value);
  } else {
    // no logueado: forzamos modo texto
    seleccion.value = "texto";
  }
});

function formateaDir(d) {
  const partes = [d.calle, d.colonia, d.ciudad].filter(Boolean);
  const base = partes.join(", ");
  return d.referencias ? `${base} (Ref: ${d.referencias})` : base;
}

async function armaPayload() {
  // items al formato que espera el backend
  const items = carritoItems.value.map(i => ({
    nombre_producto: i.nombre,
    cantidad: 1,
    toppings: i.toppings || [],
    sin_ingredientes: i.sin_ingredientes || [],
    subtotal: i.total
  }));

  // valida nombre y teléfono
  if (!form.value.nombre || !form.value.telefono) {
    throw new Error("Faltan nombre y/o teléfono");
  }
  if (!items.length) {
    throw new Error("El carrito está vacío");
  }

  const base = {
    user_id: userId.value ? Number(userId.value) : null,
    nombre: form.value.nombre,
    telefono: form.value.telefono,
    total: Number(totalCarrito.value).toFixed(2),
    pedido: items
  };

  // Caso A: no logueado → solo texto
  if (!userId.value || seleccion.value === "texto") {
    if (!direccionTexto.value.trim()) {
      throw new Error("Falta la dirección de entrega");
    }
    return { ...base, direccion_entrega: direccionTexto.value.trim() };
  }

  // Caso B: logueado + elige una guardada
  if (seleccion.value?.startsWith("id:")) {
    const id = Number(seleccion.value.split(":")[1]);
    if (!id) throw new Error("Dirección seleccionada inválida");
    // importante: si mandas id, NO mandes texto
    return { ...base, direccion_id: id };
  }

  // Caso C: logueado + nueva dirección
  if (seleccion.value === "nueva") {
    const partes = [nueva.value.calle, nueva.value.colonia, nueva.value.ciudad].filter(Boolean);
    if (!partes.length) throw new Error("Completa al menos calle, colonia y ciudad");
    const snap = nueva.value.referencias ? `${partes.join(", ")}, Ref: ${nueva.value.referencias}` : partes.join(", ");

    // ¿guardar?
    if (nueva.value.guardar) {
      const creado = await crearDireccion({
        user_id: Number(userId.value),
        calle: nueva.value.calle,
        colonia: nueva.value.colonia,
        ciudad: nueva.value.ciudad,
        referencias: nueva.value.referencias
      });
      if (creado && (creado.id || creado.direccion_id)) {
        return { ...base, direccion_id: creado.id || creado.direccion_id };
      }
      // si no se pudo guardar, al menos manda snapshot de texto
    }
    return { ...base, direccion_entrega: snap };
  }

  // fallback si no eligió nada
  throw new Error("Selecciona una dirección o escribe la dirección de entrega");
}

async function confirmarPedido() {
  let payload;
  try {
    payload = await armaPayload();
  } catch (e) {
    alert(e.message);
    return;
  }

  const resp = await crearPedido(payload);
  if (!resp.ok) {
    alert(resp.error || "No se pudo crear el pedido");
    return;
  }
  dataPedido.value = resp.data;

  if (abrirWhatsAuto.value) enviarAlNegocio();
}

function enviarAlNegocio() {
  if (!dataPedido.value) return;
  abrirWhatsResumen({
    to: NEGOCIO_TEL,
    pedidoId: dataPedido.value.pedido_id,
    nombre: form.value.nombre,
    telefono: form.value.telefono,
    items: (carritoItems.value || []).map(i => ({
      nombre_producto: i.nombre,
      cantidad: 1,
      subtotal: i.total,
      toppings: i.toppings || [],
      sin_ingredientes: i.sin_ingredientes || []
    })),
    total: dataPedido.value.total,
    direccionEntrega: dataPedido.value.direccion_entrega
  });
}

function compartirConCliente() {
  if (!dataPedido.value) return;
  const to = telefonoParaWhats(form.value.telefono);
  if (!to) return alert("Falta teléfono del cliente o es inválido");
  abrirWhatsResumen({
    to,
    pedidoId: dataPedido.value.pedido_id,
    nombre: form.value.nombre,
    telefono: form.value.telefono,
    items: (carritoItems.value || []).map(i => ({
      nombre_producto: i.nombre,
      cantidad: 1,
      subtotal: i.total,
      toppings: i.toppings || [],
      sin_ingredientes: i.sin_ingredientes || []
    })),
    total: dataPedido.value.total,
    direccionEntrega: dataPedido.value.direccion_entrega
  });
}

</script>


<template>
  <div style="padding:16px">
    <h1>Checkout</h1>

    <label>Nombre: <input v-model="form.nombre" /></label><br>
    <label>Teléfono: <input v-model="form.telefono" /></label><br>

    <!-- Direcciones -->
    <div style="margin:12px 0;">
      <template v-if="userId">
        <label>Dirección de entrega:</label><br>
        <select v-model="seleccion" style="min-width:280px">
          <option disabled value="">Selecciona una dirección</option>
          <option v-for="d in direcciones" :key="d.id" :value="`id:${d.id}`">
            {{ formateaDir(d) }}
          </option>
          <option value="nueva">+ Nueva dirección...</option>
          <option value="texto">Usar texto libre</option>
        </select>
        <p v-if="userId && direcciones.length === 0" style="margin-top:6px">
            No tienes direcciones guardadas aún.
        </p>
        <!-- Nueva dirección -->
        <div v-if="seleccion==='nueva'" style="margin-top:8px; display:grid; gap:6px; max-width:420px">
          <input v-model="nueva.calle" placeholder="Calle y número">
          <input v-model="nueva.colonia" placeholder="Colonia">
          <input v-model="nueva.ciudad" placeholder="Ciudad">
          <input v-model="nueva.referencias" placeholder="Referencias (opcional)">
          <label><input type="checkbox" v-model="nueva.guardar"> Guardar esta dirección</label>
        </div>

        <!-- Texto libre (logueado pero quiere capturar texto puntual) -->
        <div v-if="seleccion==='texto'" style="margin-top:8px; max-width:420px">
          <textarea v-model="direccionTexto" placeholder="Escribe la dirección de entrega"></textarea>
        </div>
      </template>

      <template v-else>
        <!-- No logueado: solo texto -->
        <label>Dirección de entrega:</label><br>
        <textarea v-model="direccionTexto" placeholder="Escribe la dirección de entrega" style="min-width:280px"></textarea>
      </template>
    </div>

    <p>Total: ${{ Number(totalCarrito).toFixed(2) }}</p>

    <button @click="confirmarPedido">Confirmar pedido</button>

    <label class="ml-2">
      <input type="checkbox" v-model="abrirWhatsAuto" />
      Abrir Whats al crear pedido
    </label>

    <!-- <div v-if="dataPedido" class="mt-3" style="display:flex; gap:8px">
      <button @click="enviarAlNegocio">Enviar al negocio</button>
      <button @click="compartirConCliente">Compartir con el cliente</button>
    </div> -->
  </div>
</template>
