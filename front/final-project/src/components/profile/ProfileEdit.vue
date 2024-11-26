<template>
  <form @submit.prevent="handleSubmit" class="edit-form">
    <div class="profile-image-container">
      <img 
        :src="imagePreview || getProfileImageUrl(initialData?.profile_img)" 
        alt="프로필 이미지" 
        class="profile-image"
      >
      <input 
        type="file" 
        @change="handleImageChange" 
        accept="image/*"
      >
    </div>
    <div class="form-group">
      <label>닉네임:</label>
      <input type="text" v-model="editForm.nickname" class="form-control">
    </div>

    <div class="form-group">
      <label>연락처:</label>
      <input type="text" v-model="editForm.phone" class="form-control">
    </div>

    <div class="form-group">
      <label>나이:</label>
      <input type="number" v-model="editForm.age" class="form-control" min="0">
    </div>

    <div class="form-group">
      <label>자산 (원):</label>
      <input type="number" v-model="editForm.property" class="form-control" min="0">
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
  nickname: '',
  phone: '',
  age: '',
  property: '',
  marital_status: false,
  gender: 'N',
})

const imagePreview = ref(null)
const imageFile = ref(null)

const getProfileImageUrl = (profileImg) => {
  if (!profileImg) {
    return 'http://localhost:8000/media/profile_images/default_profile.png'
  }
  return `http://localhost:8000${profileImg}`
}

onMounted(() => {
  // 초기 데이터로 폼 초기화
  editForm.value = {
    nickname: props.initialData?.nickname || '',
    phone: props.initialData?.phone || '',
    age: props.initialData?.age || '',
    property: props.initialData?.property || '',
    marital_status: props.initialData?.marital_status || false,
    gender: props.initialData?.gender || 'N',
  }
})

const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

const handleSubmit = () => {
  const formData = new FormData()
  
  if (imageFile.value) {
    formData.append('profile_img', imageFile.value)
  }
  
  // 다른 폼 데이터 추가
  formData.append('nickname', editForm.value.nickname)
  formData.append('phone', editForm.value.phone)
  formData.append('age', editForm.value.age)
  formData.append('property', editForm.value.property)
  formData.append('marital_status', editForm.value.marital_status)
  formData.append('gender', editForm.value.gender)
  
  emit('submit', formData)
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

.profile-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 50%;
}

.profile-image-container {
  margin-bottom: 1rem;
  text-align: center;
}
</style> 