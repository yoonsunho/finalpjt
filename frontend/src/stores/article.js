import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './user'

export const useArticleStore = defineStore('article', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const articles = ref([])
  const articleDetail = ref(null)
  const comments = ref([])
  const accountStore = useAccountStore()

  const getArticles = function (category = 'REVIEW') {
    axios({
      method: 'GET',
      url: `${API_URL}/community/?category=${category}`,
    })
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const getArticleDetail = function (id) {
    articleDetail.value = null
    axios({
      method: 'GET',
      url: `${API_URL}/community/${id}`,
    })
      .then((res) => {
        articleDetail.value = res.data
        // return res.data
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const createArticle = (data) => {
    return axios({
      method: 'POST',
      url: `${API_URL}/community/create`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
      data,
    })
  }

  const updateArticle = (articleId, data) => {
    return axios({
      method: 'PUT',
      url: `${API_URL}/community/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
      data,
    })
  }

  const deleteArticle = (articleId) => {
    return axios({
      method: 'DELETE',
      url: `${API_URL}/community/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  const toggleLike = (articleId) => {
    if (!accountStore.isLogin) return
    axios
      .post(
        `${API_URL}/community/${articleId}/like/`,
        {},
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        },
      )
      .then(() => {
        getArticleDetail(articleId)
      })
      .catch((err) => {
        console.error('좋아요 실패:', err)
      })
  }

  const newComment = ref('')
  const editCommentId = ref(null)
  const editContent = ref('')

  const getComments = (articleId) => {
    axios
      .get(`${API_URL}/community/${articleId}/comments/`)
      .then((res) => {
        comments.value = res.data
      })
      .catch((err) => {
        console.error(err)
      })
  }

  const createComment = () => {
    if (!articleDetail.value) return
    axios
      .post(
        `${API_URL}/community/${articleDetail.value.id}/comments/`,
        {
          content: newComment.value,
        },
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        },
      )
      .then(() => {
        getComments(articleDetail.value.id)
        newComment.value = ''
      })
      .catch((err) => {
        console.error('댓글 작성 실패:', err.response?.data || err)
      })
  }

  const startEdit = (comment) => {
    editCommentId.value = comment.id
    editContent.value = comment.content
  }

  const updateComment = (commentId) => {
    axios
      .put(
        `${API_URL}/community/comments/${commentId}/`,
        {
          content: editContent.value,
        },
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        },
      )
      .then((res) => {
        const idx = comments.value.findIndex((c) => c.id === commentId)
        if (idx !== -1) comments.value[idx] = res.data
        editCommentId.value = null
      })
      .catch((err) => {
        console.error('댓글 수정 실패:', err.response?.data || err)
      })
  }

  const deleteComment = (commentId) => {
    axios
      .delete(`${API_URL}/community/comments/${commentId}/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
      .then(() => {
        comments.value = comments.value.filter((c) => c.id !== commentId)
      })
      .catch((err) => {
        console.error('댓글 삭제 실패:', err.response?.data || err)
      })
  }

  return {
    API_URL,
    articles,
    articleDetail,
    comments,
    newComment,
    editCommentId,
    editContent,

    getArticles,
    getArticleDetail,
    createArticle,
    updateArticle,
    deleteArticle,
    toggleLike,

    getComments,
    createComment,
    startEdit,
    updateComment,
    deleteComment,
  }
})
