<template>
  <div>
    <p class="cursor" @click.prevent="goBack">← 뒤로가기</p>
    <h2>{{ detail.fin_prdt_nm }}</h2>
    <p>{{ detail.kor_co_nm }}</p>
    <!-- <span
      v-for="option in detail.option"
    >{{ option.save_trm }}개월</span><br><br> -->
    <p>최고 한도 : {{ detail.max_limit ? detail.max_limit : '없음' }}</p>
    <p>가입 대상 : {{ detail.join_member }}</p>
    <p>가입 제한 : {{ joinDeny() }}</p>
    <p>가입 방법 : {{ detail.join_way }}</p>
    <p>상세 정보</p>
    <p>{{ detail.etc_note }}</p>
    <p>우대 조건</p>
    <p>{{ detail.spcl_cnd }}</p>
    <div class="option-detail">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">기간</th>
            <th scope="col">금리 유형</th>
            <th scope="col">저축 금리</th>
            <th scope="col">최고 우대금리</th>
          </tr>
        </thead>
  
        <tbody>
          <tr
            v-for="option in options"
          >
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance';
const store = useFinanceStore()

const detail = store.detail

const options = detail.option.sort(function (a, b) {
  const optionA = a.save_trm;
  const optionB = b.save_trm;

  if (optionA && optionB) {
    return optionA - optionB;
  } else if (optionA) {
    return 1;
  } else if (optionB) {
    return -1;
  } else {
    return 0;
  }
});
const joinDeny = function () {
  if (detail.join_deny === 1) {
    return '제한 없음'
  }
  else if (detail.join_deny === 2) {
    return '서민 전용'
  }
  else {
    return '일부 제한'
  }
}

const goBack = () => {
  store.goBack()
}

</script>

<style scoped>
td {
  width: 20px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.cursor {
  cursor: pointer;
}
.option-detail {
  width: 600px;
}
</style>