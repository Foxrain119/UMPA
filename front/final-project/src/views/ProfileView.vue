<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>프로필 정보</h2>
      
      <ProfileInfo 
        v-if="!store2.isEditing" 
        :profile="store2.profile"
        @start-edit="startEdit"
      />

      <ProfileEdit
        v-else
        :initial-data="store2.profile"
        @submit="handleSubmit"
        @cancel="cancelEdit"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import ProfileInfo from '@/components/profile/ProfileInfo.vue'
import ProfileEdit from '@/components/profile/ProfileEdit.vue'

const store2 = useAccountStore()

onMounted(async () => {
  await store2.getProfile()
})

const startEdit = () => {
  store2.isEditing = true
}

const cancelEdit = () => {
  store2.isEditing = false
}

const handleSubmit = async (userData) => {
  await store2.updateProfile(userData)
}

// 컴포넌트가 언마운트될 때 수정 모드 초기화
onUnmounted(() => {
  store2.isEditing = false
})
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>