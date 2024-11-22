<template>
  <div>
    <div class="txt_box">
      <RouterLink to="algo1">추천 알고리즘 1</RouterLink> |
      <RouterLink >추천 알고리즘 2</RouterLink>
    </div>
    <RouterView />
  </div>
</template>

<script setup>

</script>

<style scoped>
.txt_box {
  text-align: center;
}
</style>