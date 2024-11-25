<template>
  <div class="chat-container">
    <h2>GPT 예적금 추천 챗봇</h2>
    <div class="chat-box">
      <div v-for="(message, index) in chatMessages" :key="index">
        <p :class="message.type">{{ message.text }}</p>
      </div>
    </div>
    <input
      v-model="userMessage"
      @keyup.enter.prevent="sendMessage"
      placeholder="메시지를 입력하세요..."
    />
    <button @click.prevent="sendMessage">보내기</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userMessage: "",
      chatMessages: [],
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userMessage.trim()) return;

      // 사용자 메시지 추가
      this.chatMessages.push({ type: "user", text: this.userMessage });

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/financial/chatbot/",
          { message: this.userMessage },
          { headers: { "Content-Type": "application/json" } }
        );

        console.log(response)
        // GPT 응답 추가
        this.chatMessages.push({ type: "bot", text: response.data.choices[0].message.content });
        // this.chatMessages.push({ type: "bot", text: response.data.message });
        console.log(this.chatMessages)
      } catch (error) {
        console.error("Error:", error);
        this.chatMessages.push({ type: "bot", text: "오류가 발생했습니다. 다시 시도해주세요." });
      } finally {
        this.userMessage = ""; // 입력 필드 초기화
      }
    },
  },
};
</script>

<style>
.chat-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.chat-box {
  height: 400px;
  overflow-y: auto;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  background: #f9f9f9;
}

p.user {
  text-align: right;
  background-color: #d1e7dd;
  padding: 5px 10px;
  margin: 5px 0;
  border-radius: 10px;
  display: inline-block;
}

p.bot {
  text-align: left;
  background-color: #f8d7da;
  padding: 5px 10px;
  margin: 5px 0;
  border-radius: 10px;
  display: inline-block;
}

input {
  width: calc(100% - 80px);
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
}
</style>
