<template>
  <ErrorPage 
    type="notFound"
    title="페이지를 찾을 수 없습니다"
    message="요청하신 페이지가 존재하지 않거나 이동했을 수 있습니다."
  />
</template>

<script setup lang="ts">
import ErrorPage from '@/components/ErrorPage.vue'
</script>
