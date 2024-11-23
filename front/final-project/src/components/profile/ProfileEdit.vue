<template>
  <form @submit.prevent="handleSubmit" class="edit-form">
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
      <button type="button" @click="$emit('cancel')" class="cancel-btn">취소</button>
    </div>

    <div class="delete-account">
      <button type="button" @click.prevent="confirmDelete" class="delete-btn">
        회원 탈퇴
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRouter } from 'vue-router'

const store2 = useAccountStore()
const router = useRouter()

const props = defineProps({
  initialData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['submit', 'cancel'])

const editForm = ref({
  age: '',
  property: '',
  marital_status: false,
  gender: 'N',
})

onMounted(() => {
  // 초기 데이터로 폼 초기화
  editForm.value = {
    age: props.initialData?.age || '',
    property: props.initialData?.property || '',
    marital_status: props.initialData?.marital_status || false,
    gender: props.initialData?.gender || 'N',
  }
})

const handleSubmit = () => {
  // 유효성 검사
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

  emit('submit', userData)
}

const confirmDelete = async () => {
  const isConfirmed = window.confirm('정말 탈퇴하시겠습니까?')
  
  if (isConfirmed) {
    try {
      await store2.deleteAccount()
      window.alert('회원탈퇴가 완료되었습니다.')
      router.push({ name: 'home' })
    } catch (error) {
      window.alert('회원탈퇴에 실패했습니다. 다시 시도해주세요.')
      console.error('회원탈퇴 오류:', error)
    }
  }
}
</script>

<style scoped>
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

.save-btn, .cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn {
  background: #28a745;
  color: white;
}

.cancel-btn {
  background: #dc3545;
  color: white;
}

.delete-account {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd;
  text-align: right;
}

.delete-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #6c757d;
  color: white;
  font-size: 0.9rem;
}

.delete-btn:hover {
  background: #dc3545;
}
</style> 