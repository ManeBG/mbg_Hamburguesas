<script setup>
import { ref, computed, onMounted } from "vue";
import { crearPedido } from "@/api/pedidos";
import { listarDirecciones, crearDireccion } from "@/api/direcciones";
import { abrirWhatsResumen, telefonoParaWhats } from "@/utils/whats";
import { carrito, vaciarCarrito } from "@/store";
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

const form = ref({ nombre: "", telefono: "" });
const userId = ref(localStorage.getItem("user_id") || null);
const router = useRouter()

const carritoItems = carrito;
const totalCarrito = computed(() => carritoItems.value.reduce((a, i) => a + Number(i.total || 0), 0));
const dataPedido = ref(null);
const abrirWhatsAuto = ref(true);
const NEGOCIO_TEL = import.meta.env.VITE_NEGOCIO_TEL;

const direcciones = ref([]);
const seleccion = ref("");
const nueva = ref({ calle:"", colonia:"", ciudad:"", referencias:"", guardar:true });
const direccionTexto = ref("");

onMounted(async () => {
  const nombreLS = localStorage.getItem("nombre"); 
  const telLS = localStorage.getItem("telefono");
  if (nombreLS) form.value.nombre = nombreLS;
  if (telLS) form.value.telefono = telLS;

  if (userId.value) {
    direcciones.value = await listarDirecciones(userId.value);
  } else {
    seleccion.value = "texto";
  }
});

function formateaDir(d) {
  const partes = [d.calle, d.colonia, d.ciudad].filter(Boolean);
  const base = partes.join(", ");
  return d.referencias ? `${base} (Ref: ${d.referencias})` : base;
}

async function armaPayload() {
  const items = carritoItems.value.map(i => ({
    nombre_producto: i.nombre,
    cantidad: 1,
    toppings: i.toppings || [],
    sin_ingredientes: i.sin_ingredientes || [],
    subtotal: i.total
  }));

  if (!form.value.nombre || !form.value.telefono) throw new Error("Faltan nombre y/o teléfono");
  if (!items.length) throw new Error("El carrito está vacío");

  const base = {
    user_id: userId.value ? Number(userId.value) : null,
    nombre: form.value.nombre,
    telefono: form.value.telefono,
    total: Number(totalCarrito.value).toFixed(2),
    pedido: items
  };

  if (!userId.value || seleccion.value === "texto") {
    if (!direccionTexto.value.trim()) throw new Error("Falta la dirección de entrega");
    return { ...base, direccion_entrega: direccionTexto.value.trim() };
  }

  if (seleccion.value?.startsWith("id:")) {
    const id = Number(seleccion.value.split(":")[1]);
    if (!id) throw new Error("Dirección seleccionada inválida");
    return { ...base, direccion_id: id };
  }

  if (seleccion.value === "nueva") {
    const partes = [nueva.value.calle, nueva.value.colonia, nueva.value.ciudad].filter(Boolean);
    if (!partes.length) throw new Error("Completa al menos calle, colonia y ciudad");
    const snap = nueva.value.referencias ? `${partes.join(", ")}, Ref: ${nueva.value.referencias}` : partes.join(", ");

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
    }
    return { ...base, direccion_entrega: snap };
  }

  throw new Error("Selecciona una dirección o escribe la dirección de entrega");
}

const enviando = ref(false);
const pedidoConfirmado = ref(false);
const yaAbriWhats = ref(false);

async function confirmarPedido() {
  if (enviando.value || pedidoConfirmado.value) return;
  try {
    enviando.value = true;
    const payload = await armaPayload();
    const resp = await crearPedido(payload);

    if (!resp.ok) {
      await Swal.fire({
        icon: 'error',
        title: 'No se pudo crear el pedido',
        text: resp.error || 'Ocurrió un problema',
      });
      return;
    }

    dataPedido.value = resp.data;
    pedidoConfirmado.value = true;

    if (abrirWhatsAuto.value) enviarAlNegocio();
  } catch (e) {
    const msg = String(e?.message || e);
    if (msg.includes('Selecciona una dirección') || msg.includes('Falta la dirección de entrega')) {
      await Swal.fire({
        icon: 'warning',
        title: 'Falta la dirección',
        html: 'Elige una <b>dirección guardada</b>, crea una <b>nueva</b> o escribe la <b>dirección en texto</b>.',
        confirmButtonText: 'Entendido',
      });
    } else {
      await Swal.fire({
        icon: 'error',
        title: 'No se puede confirmar',
        text: msg,
      });
    }
  } finally {
    enviando.value = false;
  }
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
  yaAbriWhats.value = true;
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

async function nuevoPedido({ limpiar = true, pedirConfirmacion = true, irMenu = true } = {}) {
  try {
    if (limpiar && pedirConfirmacion) {
      const { isConfirmed } = await Swal.fire({
        title: '¿Limpiar carrito para un nuevo pedido?',
        showCancelButton: true,
        confirmButtonText: 'Sí, limpiar',
        cancelButtonText: 'Cancelar'
      })
      if (!isConfirmed) return
    }
    if (limpiar) { try { vaciarCarrito() } catch {} }

    dataPedido.value = null
    pedidoConfirmado.value = false
    yaAbriWhats.value = false
    seleccion.value = userId.value ? '' : 'texto'
    direccionTexto.value = ''
    nueva.value = { calle:'', colonia:'', ciudad:'', referencias:'', guardar:true }

    if (irMenu) await router.push('/').catch(() => {})
  } catch (e) {
    console.error(e)
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="card checkout-card w-100" style="max-width: 600px; margin:auto;">
      <div class="card-body">
        <h2 class="card-title mb-4 text-center text-warning">Checkout</h2>

        <!-- Datos del cliente -->
        <div class="mb-3">
          <label class="form-label">Nombre</label>
          <input v-model="form.nombre" class="form-control" placeholder="Tu nombre" />
        </div>
        <div class="mb-3">
          <label class="form-label">Teléfono</label>
          <input v-model="form.telefono" class="form-control" placeholder="Ej: 7441234567" />
        </div>

        <!-- Direcciones -->
        <div class="mb-3">
          <label class="form-label">Dirección de entrega</label>
          <template v-if="userId">
            <select v-model="seleccion" class="form-select mb-2">
              <option disabled value="">Selecciona una dirección</option>
              <option v-for="d in direcciones" :key="d.id" :value="`id:${d.id}`">
                {{ formateaDir(d) }}
              </option>
              <option value="nueva">+ Nueva dirección...</option>
              <option value="texto">Usar texto libre</option>
            </select>

            <div v-if="seleccion==='nueva'" class="row g-2 mb-2">
              <div class="col-md-6">
                <input v-model="nueva.calle" class="form-control" placeholder="Calle y número" />
              </div>
              <div class="col-md-6">
                <input v-model="nueva.colonia" class="form-control" placeholder="Colonia" />
              </div>
              <div class="col-md-6">
                <input v-model="nueva.ciudad" class="form-control" placeholder="Ciudad" />
              </div>
              <div class="col-md-6">
                <input v-model="nueva.referencias" class="form-control" placeholder="Referencias" />
              </div>
              <div class="form-check mt-2">
                <input class="form-check-input" type="checkbox" v-model="nueva.guardar" />
                <label class="form-check-label">Guardar esta dirección</label>
              </div>
            </div>

            <textarea v-if="seleccion==='texto'" v-model="direccionTexto" class="form-control" rows="2" placeholder="Escribe la dirección completa"></textarea>
          </template>

          <template v-else>
            <textarea v-model="direccionTexto" class="form-control" rows="2" placeholder="Escribe la dirección completa"></textarea>
          </template>
        </div>

        <!-- Total -->
        <div class="alert alert-info text-center fw-bold">
          Total a pagar: ${{ Number(totalCarrito).toFixed(2) }}
        </div>

        <!-- Botones principales -->
        <div class="d-grid gap-2">
          <button class="btn btn-success btn-lg" @click="confirmarPedido" :disabled="enviando || pedidoConfirmado">
            {{ enviando ? 'Enviando...' : (pedidoConfirmado ? 'Pedido creado' : 'Confirmar pedido') }}
          </button>
          <div class="form-check text-center">
            <input type="checkbox" class="form-check-input me-2" v-model="abrirWhatsAuto" />
            <label class="form-check-label">Abrir WhatsApp al confirmar</label>
          </div>
        </div>

        <!-- Después de confirmar -->
        <div v-if="dataPedido" class="d-flex justify-content-center gap-2 mt-3">
          <button class="btn btn-primary" @click="enviarAlNegocio">
            {{ yaAbriWhats ? 'Reenviar al negocio' : 'Enviar al negocio' }}
          </button>
          <button class="btn btn-outline-secondary" type="button" @click="nuevoPedido({ limpiar:true, pedirConfirmacion:true, irMenu:true })">
            Nuevo pedido
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
