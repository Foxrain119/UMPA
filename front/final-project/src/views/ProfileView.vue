<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>프로필 정보</h2>
      
      <!-- 수정 모드가 아닐 때 -->
      <div v-if="!store2.isEditing" class="profile-info">
        <p><strong>이름:</strong> {{ store2.profile?.username }}</p>
        <p><strong>이메일:</strong> {{ store2.profile?.email }}</p>
        <p><strong>나이:</strong> {{ store2.profile?.age }}</p>
        <p><strong>자산:</strong> {{ store2.profile?.property }}만원</p>
        <p><strong>결혼여부:</strong> {{ store2.profile?.marital_status ? '기혼' : '미혼' }}</p>
        <p><strong>성별:</strong> {{ store2.profile?.gender === 'M' ? '남성' : store2.profile?.gender === 'F' ? '여성' : '' }}</p>
        
        <button @click="startEdit" class="edit-btn">
          정보 수정
        </button>
      </div>

      <!-- 수정 모드일 때 -->
      <form v-else @submit.prevent="handleSubmit" class="edit-form">
        <div class="form-group">
          <label>나이:</label>
          <input 
            type="number" 
            v-model="editForm.age" 
            class="form-control"
            min="0"
          >
        </div>

        <div class="form-group">
          <label>자산 (만원):</label>
          <input 
            type="number" 
            v-model="editForm.property" 
            class="form-control"
            min="0"
          >
        </div>

        <div class="form-group">
          <label>결혼여부:</label>
          <select v-model="editForm.marital_status" class="form-control">
            <option :value="false">미혼</option>
            <option :value="true">기혼</option>
          </select>
        </div>

        <div class="form-group">
          <label>성별:</label>
          <select v-model="editForm.gender" class="form-control">
            <option value="N">선택</option>
            <option value="M">남성</option>
            <option value="F">여성</option>
          </select>
        </div>

        <div class="button-group">
          <button type="submit" class="save-btn">저장</button>
          <button type="button" @click="cancelEdit" class="cancel-btn">취소</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAccountStore } from '@/stores/account'

const store2 = useAccountStore()

onMounted(async () => {
  await store2.getProfile()  // 프로필 정보 로드 후
  // 폼 초기화
  editForm.value = {
    age: store2.profile?.age || '',
    property: store2.profile?.property || '',
    marital_status: store2.profile?.marital_status || false,
    gender: store2.profile?.gender || 'N',
  }
})

const editForm = ref({
  age: '',
  property: '',
  marital_status: false,
  gender: 'N',
})

const startEdit = () => {
  store2.isEditing = true
  // 현재 사용자 정보로 폼 초기화
  editForm.value = {
    age: store2.profile?.age || '',
    property: store2.profile?.property || '',
    marital_status: store2.profile?.marital_status || false,
    gender: store2.profile?.gender || 'N',
  }
}

const cancelEdit = () => {
  store2.isEditing = false
}

const handleSubmit = async () => {
  // 빈 칸 허용을 위해 검증 로직 수정
  if (editForm.value.gender === 'N') {
    window.alert('성별을 선택해주세요.')
    return
  }

  if (editForm.value.age && editForm.value.age < 0) {
    window.alert('나이는 0보다 작을 수 없습니다.')
    return
  }

  if (editForm.value.property && editForm.value.property < 0) {
    window.alert('자산은 0보다 작을 수 없습니다.')
    return
  }

  // 숫자 타입으로 변환 (빈 문자열이면 null로 설정)
  const userData = {
    ...editForm.value,
    age: editForm.value.age ? Number(editForm.value.age) : null,
    property: editForm.value.property ? Number(editForm.value.property) : null,
  }

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

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-group {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
}

.edit-btn, .save-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background: #007bff;
  color: white;
}

.save-btn {
  background: #28a745;
  color: white;
}

.cancel-btn {
  background: #dc3545;
  color: white;
}

.profile-info p {
  margin-bottom: 0.5rem;
}
</style>