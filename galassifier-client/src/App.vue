<script setup>
import GalaxyCard from './components/GalaxyCard.vue'

</script>

<template>
  <div class="app">
    <h1>Galassifier</h1>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 300ms ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>