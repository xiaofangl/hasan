<template>
  <aside id="left-panel">

    <el-tree :data="data" :props="defaultProps" node-key="id" @node-click="handleNodeClick"></el-tree>

  </aside>

</template>

<script>
  import routes from '../routes'

  export default {
    data() {
      return {
        items: routes,
        data: [{
          id: 1,
          label: '发布',
          children: [{id: 13, label: '发布'}]
        }, {
          id: 2,
          label: 'DNS',
          children: [{
            id: 21,
            label: '记录'
          }, {
            id: 22,
            label: '文件'
          }]
        }, {
          id: 3,
          label: 'CMDB',
          children: [{
            id: 31,
            label: '资源'
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      }
    },
    methods: {
      handleNodeClick(data) {
        // console.log(data, typeof(data.id));
        let clickId = data.id;
        switch (clickId) {
          case 1:
            break;
          case 2:
            break;
          case 3:
            break;
          default:
            let targetName = '0' + String(clickId);
            console.log('targetname', targetName)
            this.$router.push({name: targetName});
            this.$store.commit('addTab', targetName)
        }
        ;
      }
    }
  };

</script>


<style>
  .el-icon-caret-right:before {
    content: "";
  }

  aside {
    /*background: white;*/
    background: rgb(250, 253, 251);
    width: 130px;
  }

  .el-tree {
    border: 0px solid rgb(209, 229, 219)
  }
  .el-tree-node__content {
    font-weight: 700;}


</style>
