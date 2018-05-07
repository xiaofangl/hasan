<template>
  <div id="main-tabs">
    <el-tabs v-model="activeName" type="card" :closable="true" @tab-click="handleClick"
             @tab-remove="handleRemove">
      <el-tab-pane v-for="tab in tabs" :key="tab.label" :label="tab.label" :name="tab.name"></el-tab-pane>
    </el-tabs>
  </div>
</template>
<script>
  export default {
    methods: {
      handleRemove(targetName) {
        if (targetName === '001') {
          return
        }
        if (this.activeName === targetName) {
          let tabArray = this.tabs
          tabArray.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabArray[index + 1] || tabArray[index - 1];
              if (nextTab) {
                this.$store.commit('setActiveName', nextTab.name);
                this.$router.push({name: nextTab.name})
              }
            }
          })
        }
        this.$store.commit('delTab', targetName)
      },
      handleClick(tab, event) {
        this.$router.push({name: tab.name})
        console.log(this.$router)
      }
    },

    computed: {
      tabs() {
        return this.$store.getters.tabLabels
      },
      activeName: {
        get: function () {
          return this.$store.state.activeName
        },
        set: function () {
        }
      }
    }
  }
</script>
