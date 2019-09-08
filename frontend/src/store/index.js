import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    tagObject: {},
    pen: false,
    text: '',
    tags: [],
    relations: [],
    num: 1,
    totalPage: 1,
    ent1: '',
    ent2: '',
    tempId: 0,
    tempTags: [],
    show: true
  },
  getters: {
    getPen (state) {
      return state.pen
    },
    getText (state) {
      return state.text
    },
    getTags (state) {
      return state.tags
    },
    getRelations (state) {
      return state.relations
    },
    getTempId (state) {
      return state.tempId
    },
    getTempTags (state) {
      return state.tempTags
    },
    getTagObject (state) {
      return state.tagObject
    },
    getNum (state) {
      return state.num
    },
    getTotalPage (state) {
      return state.totalPage
    },
    getEnt1 (state) {
      return state.ent1
    },
    getEnt2 (state) {
      return state.ent2
    },
    getShow (state) {
      return state.show
    }
  },
  mutations: {
    setPen (state) {
      state.pen = true
    },
    unsetPen (state) {
      state.pen = false
    },
    setText (state, text) {
      state.text = text
    },
    setTags (state, tags) {
      state.tags = tags
    },
    setTagObject (state, tag) {
      state.tagObject = tag
    },
    setRelations (state, relations) {
      state.relations = relations
    },
    setTempId (state, id) {
      state.tempId = id
      if (state.show === false) {
        let temp = []
        let text1 = state.relations[state.tempId].em1Text
        let text2 = state.relations[state.tempId].em2Text
        for (let i of state.tempTags) {
          if (i['text'] === text1) {
            temp.push(i)
          }
          if (i['text'] === text2) {
            temp.push(i)
          }
        }
        state.tags = temp
      }
    },
    setTempTags (state, tags) {
      state.tempTags = tags
    },
    setNum (state, num) {
      state.num = num
    },
    setTotalPage (state, page) {
      state.totalPage = page
    },
    setEnt1 (state, ent1) {
      state.ent1 = ent1
    },
    setEnt2 (state, ent2) {
      state.ent2 = ent2
    },
    setShow (state, show) {
      state.show = show
    }
  },
  actions: {
    setPageNum (context, params) {
      params.$this.$store.commit('setNum', params.num)
      params.$this.$axios.get(params.$this.URL.getTags,
        {
          params: {
            num: params.num
          }
        })
        .then(res => {
          let tag = JSON.parse(res.data.tag)
          context.commit('setTagObject', tag)
          context.commit('setText', tag['sentText'])
          context.commit('setTags', tag['entityMentions'])
          context.commit('setTempTags', tag['entityMentions'])
          context.commit('setRelations', tag['relationMentions'])
          context.commit('setTempId', 0)
          if (context.state.show === false) {
            let temp = []
            let text1 = context.state.relations[context.state.tempId].em1Text
            let text2 = context.state.relations[context.state.tempId].em2Text
            for (let i of context.state.tempTags) {
              if (i['text'] === text1) {
                temp.push(i)
              }
              if (i['text'] === text2) {
                temp.push(i)
              }
            }
            context.commit('setTags', temp)
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
})

export default store
