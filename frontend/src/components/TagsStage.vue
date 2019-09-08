<template>
  <div class="sidebar">
    <div v-show="this.show">
      <el-button size="small" type="primary" @click="exportFile">Export</el-button>
      <el-button size="small" type="danger" @click="saveTags(num)">Save</el-button>
      <el-button type="warning" icon="el-icon-edit" @click="tag" circle></el-button>
      <div style="margin: 15px">Entity1: <span style="font-weight: bold;">{{ entity1 }}</span> -- Entity2:
        <span style="font-weight: bold;">{{ entity2 }}</span>
        <el-button style="margin-left: 50px;" size="small" type="success" @click="addRelation" :disabled="!disable">OK
        </el-button>
      </div>
      <div style="margin: 20px; font-size: large; font-weight: bold">Relations</div>
      <el-card v-for="(relation, i) in relations" :key="i" shadow="hover" style="margin: 10px;">
        <div slot="header" style="font-weight: bold">{{ relation['em1Text'] }} - {{ relation['em2Text'] }}
          <el-button style="float: right; padding: 3px 0" type="text" @click="deleteRelation(i)">X</el-button>
        </div>
        <el-select v-model="relation['label']" placeholder="Relation" @change="selectLabel">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.value"
            :value="item.value">
          </el-option>
        </el-select>
        <el-checkbox style="margin-left: 80px;" v-model="relation['is_noise']" @change="selectLabel">Noise?
        </el-checkbox>
      </el-card>
      <div style="margin: 20px; font-size: large; font-weight: bold">Tags</div>
      <el-table
        :data="tags"
        style="margin: 10px">
        <el-table-column
          prop="text"
          label="Text"
          width="260">
        </el-table-column>
        <el-table-column
          label="Label"
          width="260">
          <template slot-scope="scope">
            <el-select v-model="scope.row.label" placeholder="Type" @change="selectType">
              <el-option
                v-for="item in typeOptions"
                :key="item.value"
                :label="item.value"
                :value="item.value">
              </el-option>
            </el-select>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div v-show="!show" v-if="relations[id]">
      <el-card shadow="hover" style="margin: 10px;">
        <div slot="header" style="font-weight: bold">{{ relations[id]['em1Text'] }} - {{ relations[id]['em2Text'] }}
          <el-button style="float: right; padding: 3px 0" type="text" @click="deleteRelation(i)">X</el-button>
        </div>
        <el-select v-model="relations[id]['label']" placeholder="Relation" @change="selectLabel">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.value"
            :value="item.value">
          </el-option>
        </el-select>
        <el-checkbox style="margin-left: 80px;" v-model="relations[id]['is_noise']" @change="selectLabel">Noise?
        </el-checkbox>
      </el-card>
    </div>
  </div>
</template>

<script>
import FileSaver from 'file-saver'

export default {
  name: 'TagsStage',
  computed: {
    relations: function () {
      return this.$store.getters.getRelations
    },
    tags: function () {
      return this.$store.getters.getTags
    },
    entity1: function () {
      return this.$store.getters.getEnt1
    },
    entity2: function () {
      return this.$store.getters.getEnt2
    },
    disable: function () {
      return this.entity1 !== null && this.entity1.length > 0 && this.entity2 !== null && this.entity2.length > 0
    },
    num: function () {
      return this.$store.getters.getNum
    },
    id: function () {
      return this.$store.getters.getTempId
    },
    show: function () {
      return this.$store.getters.getShow
    }
  },
  watch: {
    num: function (val, oldval) {
      this.saveTags(oldval)
      this.$store.commit('setEnt1', '')
      this.$store.commit('setEnt2', '')
    },
    show: function (val) {
      if (val === true) {
        let temp = this.$store.getters.getTempTags
        this.$store.commit('setTags', temp)
      } else {
        let temp = []
        let text1 = this.relations[this.id].em1Text
        let text2 = this.relations[this.id].em2Text
        for (let i of this.tags) {
          if (i['text'] === text1) {
            temp.push(i)
          }
          if (i['text'] === text2) {
            temp.push(i)
          }
        }
        this.$store.commit('setTags', temp)
      }
    }
  },
  data () {
    return {
      options: [
        {value: 'NA'},
        {value: '/sports/sports_team_location/teams'},
        {value: '/sports/sports_team/location'},
        {value: '/business/company/major_shareholders'},
        {value: '/business/company_shareholder/major_shareholder_of'},
        {value: '/people/person/religion'},
        {value: '/people/ethnicity/geographic_distribution'},
        {value: '/people/person/ethnicity'},
        {value: '/people/ethnicity/people'},
        {value: '/business/person/company'},
        {value: '/business/company/advisors'},
        {value: '/location/country/capital'},
        {value: '/location/location/contains'},
        {value: '/business/company/place_founded'},
        {value: '/people/person/nationality'},
        {value: '/people/person/place_lived'},
        {value: '/people/deceased_person/place_of_death'},
        {value: '/location/neighborhood/neighborhood_of'},
        {value: '/location/administrative_division/country'},
        {value: '/location/country/administrative_divisions'},
        {value: '/people/person/place_of_birth'},
        {value: '/people/person/children'},
        {value: '/business/company/founders'},
        {value: '/business/company/industry'},
        {value: '/people/person/profession'}
      ],
      typeOptions: [
        {value: 'LOCATION'},
        {value: 'ORGANIZATION'},
        {value: 'PERSON'}
      ]
    }
  },
  methods: {
    tag () {
      if (window.getSelection().baseNode.parentElement.tagName === 'P') {
        let tags = this.$store.getters.getTags
        let start = window.getSelection().anchorOffset
        let end = window.getSelection().focusOffset
        let word = window.getSelection().baseNode.data.substring(start, end)
        if (window.getSelection().baseNode.previousElementSibling && window.getSelection().baseNode.previousElementSibling.tagName === 'SPAN') {
          let tagId = parseInt(window.getSelection().baseNode.previousElementSibling.id)
          let tag = tags[tagId]
          tags.splice(tagId + 1, 0,
            {
              'start': tag.end + start,
              'end': tag.end + end,
              'label': 'LOCATION',
              'text': word
            }
          )
          this.$store.commit('setTags', tags)
          this.$store.commit('setTempTags', tags)
        } else {
          tags.splice(0, 0,
            {
              'start': start,
              'end': end,
              'label': 'LOCATION',
              'text': word
            }
          )
          this.$store.commit('setTags', tags)
          this.$store.commit('setTempTags', tags)
        }
      }
    },
    addRelation () {
      let relations = this.$store.getters.getRelations
      relations.push({
        em1Text: this.entity1,
        em2Text: this.entity2,
        label: 'NA',
        is_noise: false
      })
      this.$store.commit('setEnt1', '')
      this.$store.commit('setEnt2', '')
    },
    saveTags (num) {
      let relations = this.$store.getters.getRelations
      let tags = this.$store.getters.getTempTags
      let obj = this.$store.getters.getTagObject
      obj['entityMentions'] = tags
      obj['relationMentions'] = relations
      this.$axios.post(this.URL.saveTags,
        {
          'id': num,
          'tag': obj
        }
      ).then(res => {
      })
        .catch(error => {
          console.log(error)
        })
    },
    deleteRelation (i) {
      let relations = this.$store.getters.getRelations
      relations.splice(i, 1)
      this.$store.commit('setRelations', relations)
    },
    selectType (val) {
      this.$store.commit('setTags', this.tags)
      this.$store.commit('setTempTags', this.tags)
    },
    selectLabel (val) {
      this.$store.commit('setRelations', this.relations)
    },
    exportFile () {
      this.$axios.get(this.URL.exportFile
      ).then(res => {
        const blob = new Blob([res.data.tag], {type: ''})
        FileSaver.saveAs(blob, 'data.json')
      })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
  .sidebar {
    margin-left: 550px;
  }
</style>
