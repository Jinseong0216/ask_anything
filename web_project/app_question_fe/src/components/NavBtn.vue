<template>
  <router-link
    :to="to"
    class="px-3 h-9 flex items-center text-sm font-medium
           text-zinc-600 hover:text-zinc-900
           hover:bg-zinc-100 rounded transition"
  >
    {{ label }}
  </router-link>
</template>

<script setup>
// eslint-disable-next-line no-undef
defineProps({
  label: {
    type: String,
    required: true
  },
  to: {
    type: String,
    required: true
  }
})
</script>
