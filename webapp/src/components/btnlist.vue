<template>
  <div>
    <router-link :to="{path: item.path}" v-for="item in items" :key="item.name">
      <el-button type="primary" size="small">{{item.label}}</el-button>
    </router-link>
  </div>
</template>

<script>
  export default {
    props: {
      items: {
        type: Array,
        default: function () {
          return []
        }
      }
    }
  }
</script>
