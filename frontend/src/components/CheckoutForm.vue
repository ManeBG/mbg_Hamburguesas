<!-- src/components/CheckoutForm.vue -->
<script setup>
const props = defineProps({ form: Object })
const emit = defineEmits(['submit'])
const onSubmit = () => emit('submit')
</script>

<template>
  <form class="form-grid" @submit.prevent="onSubmit">
    <div>
      <label>Nombre</label>
      <input class="input" v-model="form.nombre" required />
    </div>
    <div>
      <label>Teléfono</label>
      <input class="input" v-model="form.telefono" inputmode="tel" required />
    </div>
    <div class="form-full">
      <label>Dirección (o selecciona guardada)</label>
      <textarea class="textarea" rows="3" v-model="form.direccion"></textarea>
    </div>
    <div class="form-full">
      <button class="btn btn-primary" type="submit">Confirmar pedido</button>
    </div>
  </form>
</template>
