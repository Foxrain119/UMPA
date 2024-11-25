<template>
  <div class="profile-container">
    <div class="profile-nav">
      <div class="nav-links">
        <button 
          :class="['nav-link', { active: currentTab === 'info' }]"
          @click="currentTab = 'info'"
        >
          회원 정보 관리
        </button>
        <button 
          :class="['nav-link', { active: currentTab === 'products' }]"
          @click="currentTab = 'products'"
        >
          가입 상품 관리
        </button>
      </div>
    </div>

    <div class="profile-content">
      <div v-if="currentTab === 'info'" class="profile-card">
        <h2>회원 정보 관리</h2>
        
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

      <!-- 가입 상품 관리 탭 -->
      <div v-else-if="currentTab === 'products'" class="profile-card">
        <h2>가입 상품 관리</h2>
        <ProfileProducts 
          :profile="store2.profile"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import ProfileInfo from '@/components/profile/ProfileInfo.vue'
import ProfileEdit from '@/components/profile/ProfileEdit.vue'
import ProfileProducts from '@/components/profile/ProfileProducts.vue'

const store2 = useAccountStore()
const currentTab = ref('info')

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

onUnmounted(() => {
  store2.isEditing = false
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.profile-nav {
  margin-bottom: 2rem;
  border-bottom: 1px solid #ddd;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  padding: 1rem 2rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 1.1rem;
  color: #666;
  position: relative;
}

.nav-link.active {
  color: #0066cc;
  font-weight: bold;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #0066cc;
}

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>