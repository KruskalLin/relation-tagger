<template>
  <div id="app">
    <el-button size="small" type="primary" @click="expert">Expert</el-button>
    <TextStage/>
    <TagsStage/>
  </div>
</template>

<script>
import TextStage from './components/TextStage'
import TagsStage from './components/TagsStage'

export default {
  name: 'App',
  components: {
    TextStage,
    TagsStage
  },
  mounted () {
    this.fetchNum()
  },
  methods: {
    async fetchNum () {
      return this.$axios.get(this.URL.getTagsNum)
        .then(res => {
          this.$store.commit('setTotalPage', res.data.num)
          this.$store.dispatch('setPageNum', { $this: this, num: 1 })
        })
        .catch(error => {
          console.log(error)
        })
    },
    expert () {
      this.$store.commit('setShow', !this.$store.getters.getShow)
    }
  }
}
</script>

<style>
#app {
  justify-content: center;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 100px;
}
</style>
