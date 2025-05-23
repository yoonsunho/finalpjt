import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const articles = ref([])
  const articleDetail = ref(null)
  // const isLiked = '유저가 좋아요를했는가..?'

  // article 가져오기
  const getArticles = function () {
    axios({
      method: 'GET',
      url: `${API_URL}/community/`,
    })
      .then((res) => {
        console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getArticleDetail = function (id) {
    axios({
      method: 'GET',
      url: `${API_URL}/community/${id}`,
    })
      .then((res) => {
        console.log(res.data)
        articleDetail.value = res.data
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const toggleLike = function (articleId) {
    axios({
      method: 'POST',
      url: `${API_URL}/community/${articleId}/like`,
    })
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => console.error(err))
  }

  return {
    API_URL,
    articles,
    getArticles,
    articleDetail,
    getArticleDetail,
    toggleLike,
    // isLiked,
  }
})
