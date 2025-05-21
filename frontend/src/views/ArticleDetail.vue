<template>
    <div class="article-container">
        <div class="article-header">
            <p class="article-category"># 적금가입후기</p>
            <h1 class="article-title">제목입니다제목입니다제목입닏</h1>
            <p class="username">이다예바보</p>
            <p class="created_at">2025-10-20</p>
        </div>
        <div class="article-content">
            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Nostrum, aliquid odit, nulla non vero ipsam rem aspernatur molestias illum eos accusantium porro amet ratione sit in quasi consequatur voluptate. Atque.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Nostrum, aliquid odit, nulla non vero ipsam rem aspernatur molestias illum eos accusantium porro amet ratione sit in quasi consequatur voluptate. Atque.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Nostrum, aliquid odit, nulla non vero ipsam rem aspernatur molestias illum eos accusantium porro amet ratione sit in quasi consequatur voluptate. Atque.
            </p>
        </div>
        <div class="article-footer"></div>
            <hr>
            <CommentComponent/>
        <div>
        </div>
    </div>
   
</template>

<script setup>
import CommentComponent from '@/components/CommentComponent.vue'
import {ref} from 'vue'

</script>

<style scoped>
.article-container {
    padding: 0px 20rem;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
.article-header {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
h1 {
    font-size: 2rem;
    font-weight: bold;
}
.created_at {
    color: #888;
    font-size: 0.8rem;
}
</style>