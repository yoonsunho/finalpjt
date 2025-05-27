import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './user'
export const useArticleStore = defineStore('article', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const accountStore = useAccountStore()

  const articles = ref([])
  const articleDetail = ref(null)
  const comments = ref([])
  const selectedCategory = ref('') // 기본값을 빈 문자열로 변경
  const selectedOrdering = ref('')

  const newComment = ref('')
  const editCommentId = ref(null)
  const editContent = ref('')

  const getArticles = (searchParams = {}) => {
    let url = `${API_URL}/community/`
    const params = new URLSearchParams()
    if (selectedCategory.value) {
      params.append('category', selectedCategory.value)
    }
    if (selectedOrdering.value) {
      params.append('ordering', selectedOrdering.value)
    }
    if (searchParams.search && searchParams.search_field) {
      params.append('search_field', searchParams.search_field)
      params.append('search', searchParams.search)
    }
    if (params.toString()) {
      url += `?${params.toString()}`
    }

    console.log('Fetching articles from:', url)

    axios
      .get(url)
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        console.error('게시글 목록 조회 실패:', err)
      })
  }

  const getArticleDetail = (id) => {
    if (!id || isNaN(parseInt(id))) {
      console.error('Invalid article ID:', id)
      return
    }

    articleDetail.value = null
    const url = `${API_URL}/community/${id}/`
    console.log('Fetching article detail from:', url) // Debug log

    axios
      .get(url)
      .then((res) => {
        articleDetail.value = res.data
      })
      .catch((err) => {
        console.error('게시글 상세 조회 실패:', err)
      })
  }

  const createArticle = (data) => {
    return axios.post(`${API_URL}/community/`, data, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  const updateArticle = (id, data) => {
    return axios.put(`${API_URL}/community/${id}/`, data, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  const deleteArticle = (id) => {
    return axios.delete(`${API_URL}/community/${id}/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    })
  }

  const toggleLike = (id) => {
    if (!accountStore.isLogin) return
    axios
      .post(
        `${API_URL}/community/${id}/like/`,
        {},
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        },
      )
      .then(() => getArticleDetail(id))
      .catch((err) => console.error('좋아요 실패:', err))
  }

  const getComments = (articleId) => {
    // Fix: Ensure we're using a numeric article ID
    if (!articleId || isNaN(parseInt(articleId))) {
      console.error('Invalid article ID for comments:', articleId)
      return
    }

    const url = `${API_URL}/community/${articleId}/comments/`
    console.log('Fetching comments from:', url) // Debug log

    axios
      .get(url)
      .then((res) => {
        comments.value = res.data
      })
      .catch((err) => console.error('댓글 조회 실패:', err))
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
      .catch((err) => console.error('댓글 작성 실패:', err))
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
      .catch((err) => console.error('댓글 수정 실패:', err))
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
      .catch((err) => console.error('댓글 삭제 실패:', err))
  }
  const popularArticlesByCategory = ref({})

  const getPopularArticlesByCategory = async () => {
    const categories = ['REVIEW', 'TIP', 'FREE']
    const result = {}

    try {
      const requests = categories.map((category) =>
        axios.get(`${API_URL}/community/`, {
          params: {
            category: category,
            ordering: 'popular',
            limit: 10,
          },
        }),
      )

      const responses = await Promise.all(requests)

      categories.forEach((category, i) => {
        result[category] = responses[i].data
      })

      popularArticlesByCategory.value = result
    } catch (err) {
      console.error('인기 글 불러오기 실패:', err)
    }
  }
  return {
    articles,
    articleDetail,
    comments,
    selectedCategory,
    selectedOrdering,
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
    popularArticlesByCategory,
    getPopularArticlesByCategory,
  }
})
