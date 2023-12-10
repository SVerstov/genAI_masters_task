<template>
  <div class="news-container">
    <el-card
        class="news-card"
        v-for="news in newsList"
        :key="news.news_id"
        shadow="hover"
    >
      <div class="news-body">
        <img :src="news.image" class="news-image" alt="News image">
        <div class="news-info">
          <h2>{{ news.title }}</h2>
          <p>{{ news.text }}</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import axios from 'axios'

const newsList = ref([])

onMounted(async () => {
  try {
    const baseUrl = `http://${window.location.hostname}:5000`;
    const response = await axios.get(`${baseUrl}/api/get_news`)
    newsList.value = response.data
  } catch (error) {
    console.error('Ошибка при получении новостей:', error)
  }
})
</script>


<style scoped>
/* Стили для десктопа (по умолчанию) */
.news-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.news-card {
  width: 100%;
  margin: 20px 0;
}

.news-body {
  display: flex;
}

.news-image {
  width: 33%;
  height: auto;
  object-fit: contain;
}

.news-info {
  flex: 1;
  padding: 0 15px;
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .news-body {
    flex-direction: column;
  }

  .news-image {
    width: 100%;
  }

  .news-info {
    padding: 15px 0;
  }
}
</style>