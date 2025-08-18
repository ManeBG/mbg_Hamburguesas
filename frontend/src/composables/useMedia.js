// src/composables/useMedia.js
import { ref, onMounted, onBeforeUnmount } from 'vue'
export function useMedia(query){
  const mm = window.matchMedia(query)
  const matches = ref(mm.matches)
  const handler = e => (matches.value = e.matches)
  onMounted(() => mm.addEventListener('change', handler))
  onBeforeUnmount(() => mm.removeEventListener('change', handler))
  return matches
}
