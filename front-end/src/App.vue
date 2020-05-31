<template>
  <div id="app">
    <UploadImage/>
  </div>
</template>

<script>
import UploadImage from './components/UploadImage.vue'

export default {
  name: 'App',
  components: {
    UploadImage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #19181F;
  margin-top: 60px;
  background-color: #19181F;
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

body {
    background-color: #19181F;
}
</style>
