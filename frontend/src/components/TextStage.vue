<template xmlns:v-contextmenu="http://www.w3.org/1999/xhtml">
  <div class="text-stage">
    <div class="sdc-article-body">
      <v-contextmenu ref="contextmenu">
        <v-contextmenu-item :disabled="disable" @click="entity1">entity1</v-contextmenu-item>
        <v-contextmenu-item :disabled="disable" @click="entity2">entity2</v-contextmenu-item>
        <v-contextmenu-item :disabled="disable" @click="deleteTags">delete</v-contextmenu-item>
      </v-contextmenu>
      <p v-html="showText" @contextmenu.prevent="over($event)" v-contextmenu:contextmenu></p>
    </div>
    <el-pagination
      v-show="show"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-size="1"
      layout="prev, pager, next, jumper"
      :total="totalPage">
    </el-pagination>
  </div>
</template>

<script>
export default {
  name: 'TextStage',
  props: {
    show: Boolean
  },
  watch: {
    show (newVal, oldVal) {
      if (newVal === false) {
        console.log(newVal)
        let $this = this
        document.onkeydown = function (e) {
          let key = e.keyCode
          if (key === 38 && $this.currentPage < $this.totalPage) {
            $this.currentPage++
            $this.handleCurrentChange($this.currentPage)
          } else if (key === 38 && $this.currentPage === $this.totalPage) {
            $this.$message({
              message: '页数上限',
              type: 'error'
            })
          } else if (key === 40 && $this.currentPage > 1) {
            $this.currentPage--
            $this.handleCurrentChange($this.currentPage)
          } else if (key === 40 && $this.currentPage === 1) {
            $this.$message({
              message: '页数下限',
              type: 'error'
            })
          } else if (key === 39 && $this.tempId < $this.relations.length - 1) {
            $this.$store.commit('setTempId', $this.tempId + 1)
          } else if (key === 39 && $this.tempId === $this.relations.length - 1) {
            $this.$message({
              message: '条数上限',
              type: 'error'
            })
          } else if (key === 37 && $this.tempId > 0) {
            $this.$store.commit('setTempId', $this.tempId - 1)
          } else if (key === 37 && $this.tempId === 0) {
            $this.$message({
              message: '条数下限',
              type: 'error'
            })
          }
        }
      } else {
        document.onkeydown = null
      }
    }
  },
  computed: {
    text: function () {
      return this.$store.getters.getText
    },
    tags: function () {
      return this.$store.getters.getTags
    },
    totalPage: function () {
      return this.$store.getters.getTotalPage
    },
    showText: function () {
      let tags = this.tags
      let text = this.text
      let tempHtml = ''
      console.log(tempHtml)
      let lastend = 0
      for (let i = 0; i < tags.length; i++) {
        let start = tags[i].start
        let end = tags[i].end
        tempHtml += text.substring(lastend, start)
        tempHtml += '<span class="annotation" id="' + i + '">' + text.substring(start, end) + '</span>'
        lastend = end
      }
      tempHtml += text.substring(lastend)
      return tempHtml
    },
    relations: function () {
      return this.$store.getters.getRelations
    },
    tempId: function () {
      return this.$store.getters.getTempId
    }
  },
  data () {
    return {
      disable: false,
      id: 0,
      hoverText: '',
      currentPage: 1
    }
  },
  methods: {
    over: function (event) {
      if (event.target.nodeName === 'SPAN') {
        this.disable = false
        this.id = parseInt(event.target.id)
        this.hoverText = event.target.innerHTML
        return
      }
      this.disable = true
    },
    deleteTags () {
      let tags = this.$store.getters.getTags
      tags.splice(this.id, 1)
      this.$store.commit('setTags', tags)
      this.$store.commit('setTempTags', tags)
    },
    entity1 () {
      this.$store.commit('setEnt1', this.hoverText)
    },
    entity2 () {
      this.$store.commit('setEnt2', this.hoverText)
    },
    handleCurrentChange (val) {
      this.$store.dispatch('setPageNum', {$this: this, num: val})
    }
  }
}
</script>

<style scoped>
  .title {
    font-size: 30px;
    margin-bottom: 50px;
  }

  .sdc-article-body {
    font-family: times, serif;
    font-size: 20px;
    line-height: 45px;
  }

  .text-stage {
    float: left;
    position: fixed;
    width: 550px;
  }

  /deep/ .annotation {
    background-color: rgba(234, 2, 26, 0.1);
    text-decoration-skip-ink: none;
    cursor: move;
    position: relative;
    user-select: none;
  }

  /deep/ .annotation:hover {
    background-color: rgba(234, 2, 26, 0.3);
  }
</style>
