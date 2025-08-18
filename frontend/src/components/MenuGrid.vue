<!-- src/components/MenuGrid.vue -->
<script setup>
import ProductCard from './ProductCard.vue'
defineProps({ productos: Array })
const emit = defineEmits(['add'])
</script>

<template>
  <section class="container" style="padding-block: 1rem;">
    <h2 style="margin-bottom:.8rem;">Menú</h2>
    <div class="menu-grid">
      <ProductCard
        v-for="p in productos"
        :key="p.id"
        :producto="p"
        @add="emit('add', $event)"
      />
    </div>
  </section>
</template>
