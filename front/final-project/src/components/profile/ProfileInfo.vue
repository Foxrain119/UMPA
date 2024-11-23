<template>
  <div class="profile-info">
    <p><strong>이름:</strong> {{ profile?.username }}</p>
    <p><strong>이메일:</strong> {{ profile?.email }}</p>
    <p><strong>나이:</strong> {{ profile?.age }}</p>
    <p><strong>자산:</strong> {{ profile?.property }}만원</p>
    <p><strong>결혼여부:</strong> {{ profile?.marital_status ? '기혼' : '미혼' }}</p>
    <p><strong>성별:</strong> {{ profile?.gender === 'M' ? '남성' : '여성' }}</p>
    
    <button @click="$emit('start-edit')" class="edit-btn">
      정보 수정
    </button>
  </div>
</template>

<script setup>
defineProps({
  profile: {
    type: Object,
    required: true
  }
})

defineEmits(['start-edit'])
</script>

<style scoped>
.profile-info p {
  margin-bottom: 0.5rem;
}

.edit-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #007bff;
  color: white;
}
</style> 