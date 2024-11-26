<template>
  <div class="profile-info">
    <img 
      :src="profileImageUrl" 
      :alt="'프로필 이미지'" 
      class="profile-image"
    >
    <p><strong>이름:</strong> {{ profile?.username }}</p>
    <p><strong>닉네임:</strong> {{ profile?.nickname }}</p>
    <p><strong>이메일:</strong> {{ profile?.email }}</p>
    <p><strong>연락처:</strong> {{ profile?.phone }}</p>
    <p><strong>나이:</strong> {{ profile?.age }}</p>
    <p><strong>자산:</strong> {{ profile?.property }}원</p>
    <p><strong>결혼여부:</strong> {{ profile?.marital_status ? '기혼' : '미혼' }}</p>
    <p><strong>성별:</strong> {{ profile?.gender === 'M' ? '남성' : '여성' }}</p>
    
    <button @click="$emit('start-edit')" class="edit-btn">
      정보 수정
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
})

const profileImageUrl = computed(() => {
  if (!props.profile?.profile_img || props.profile?.profile_img === '/media/profile_images/default_profile.png') {
    return 'http://localhost:8000/static/profile_images/default_profile.png'
  }
  return `http://localhost:8000${props.profile.profile_img}`
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

.profile-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 1rem;
}
</style> 