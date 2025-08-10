<!-- src/components/Checkout.vue -->
<script setup>
import { ref, computed } from "vue";
import { crearPedido } from "@/api/pedidos";    // lo hacemos abajo
import { abrirWhatsResumen, telefonoParaWhats } from "@/utils/whats";

const form = ref({
  nombre: "",
  telefono: "",         // input del cliente
  // ...otros campos del formulario
});

const carritoItems = ref([]);   // ya lo tienes
const totalCarrito = computed(() =>
  carritoItems.value.reduce((acc, i) => acc + Number(i.subtotal || 0), 0)
);

const dataPedido = ref(null);     // respuesta del backend
const abrirWhatsAuto = ref(true); // toggle para auto-abrir al crear el pedido
const NEGOCIO_TEL = import.meta.env.VITE_NEGOCIO_TEL;

async function confirmarPedido(payloadFinal) {
  // payloadFinal lo armas como ya lo vienes haciendo (con direccion_id o direccion_entrega)
  const resp = await crearPedido(payloadFinal);
  if (!resp.ok) {
    alert(resp.error || "No se pudo crear el pedido");
    return;
  }
  dataPedido.value = resp.data;

  // Whats automático (al negocio)
  if (abrirWhatsAuto.value) {
    enviarAlNegocio();
  }
}

function enviarAlNegocio() {
  if (!dataPedido.value) return;
  abrirWhatsResumen({
    to: NEGOCIO_TEL,
    pedidoId: dataPedido.value.pedido_id,
    nombre: form.value.nombre,
    telefono: form.value.telefono,
    items: carritoItems.value,
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
    items: carritoItems.value,
    total: dataPedido.value.total,
    direccionEntrega: dataPedido.value.direccion_entrega
  });
}
</script>

<template>
  <!-- ...tu formulario (nombre, telefono, dirección, etc.) ... -->

  <!-- Confirmar -->
  <button @click="() => confirmarPedido(armaPayload())">
    Confirmar pedido
  </button>

  <!-- Opcional: toggle -->
  <label class="ml-2">
    <input type="checkbox" v-model="abrirWhatsAuto" />
    Abrir Whats al crear pedido
  </label>

  <!-- Botones se habilitan cuando ya hay dataPedido -->
  <div v-if="dataPedido" class="mt-3 flex gap-2">
    <button @click="enviarAlNegocio">Enviar al negocio</button>
    <button @click="compartirConCliente">Compartir con el cliente</button>
  </div>
</template>
