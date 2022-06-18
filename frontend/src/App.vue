<template>
  <div id="app-nav-wrapper">
    <Navigation />
    <div id="main-container">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import Navigation from '@/components/Navigation.vue';
</script>

<style lang='scss'>
@use "@/assets/main.scss" as *;
</style>
