<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class" style="background-color: white">
        <el-card class="box-card">
          <el-tabs type="border-card" @tab-click="handleClick">
            <el-tab-pane label="添加权限">
              <el-form ref="add_form" :model="add_form" label-width="80px">
                <el-form-item label="权限组" prop="permission_group">
                  <el-select v-model="add_form.permission_group" placeholder="请选择权限组">
                    <el-option :value="item.group__name" :key="item.id" v-for="item in tableData4">
                      {{item.group__name}}
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="用户">
                  <el-table ref="multipleTable" :data="tableData1" tooltip-effect="dark" style="width: 100%"
                            @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column label="ID" width="120" prop="id">
                      <!--<template prop="id"></template>-->
                    </el-table-column>
                    <el-table-column prop="username" label="用户名" width="120">
                    </el-table-column>
                    <el-table-column prop="email" label="邮箱" show-overflow-tooltip>
                    </el-table-column>
                  </el-table>
                  <div style="margin-top: 20px">
                    <el-pagination background layout="prev, pager, next" :total="pages">
                    </el-pagination>
                    <el-button type="primary" @click="toggleSelection()">取消</el-button>
                    <el-button type="primary" @click="submitSelection()">确认添加</el-button>
                  </div>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="删除权限">
              <el-form ref="del_form" :model="del_form" label-width="80px">
                <el-form-item label="用户" prop="permission_group">
                  <el-select v-model="del_form.user" placeholder="请选择用户" @change="isGroups">
                    <el-option :value="item.username" :key="item.id" v-for="item in tableData1">{{item.username}}
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="权限组" v-if="istableData3 == 0">
                  <el-table ref="multipleTables" :data="tableData2" tooltip-effect="dark" style="width: 100%"
                            @selection-change="deleteSelectionChange">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column label="ID" width="120" prop="id">
                      <!--<template prop="id"></template>-->
                    </el-table-column>
                    <el-table-column prop="groupextend__be_app" label="APP" width="120">
                    </el-table-column>
                    <el-table-column prop="name" label="权限组" show-overflow-tooltip>
                    </el-table-column>
                  </el-table>
                  <div style="margin-top: 20px">
                    <el-pagination background layout="prev, pager, next" :total="page2">
                    </el-pagination>
                    <el-button type="primary" @click="toggleSelections()">取消</el-button>
                    <el-button type="primary" @click="submitDelete()">确认删除</el-button>
                  </div>
                </el-form-item>
                <el-form-item label="权限组" v-if="istableData3 == 1">
                  <el-table ref="multipleTable" :data="tableData3" tooltip-effect="dark" style="width: 100%"
                            @selection-change="deleteSelectionChange">
                    <el-table-column type="selection" width="55">
                    </el-table-column>
                    <el-table-column label="ID" width="120" prop="group_id">
                      <!--<template prop="group_id"></template>-->
                    </el-table-column>
                    <el-table-column prop="group__groupextend__be_app" label="APP" width="120">
                    </el-table-column>
                    <el-table-column prop="group__name" label="权限组" show-overflow-tooltip>
                    </el-table-column>
                  </el-table>
                  <div style="margin-top: 20px">
                    <el-pagination background layout="prev, pager, next" :total="page3">
                    </el-pagination>
                    <el-button type="primary" @click="toggleSelection()">取消</el-button>
                    <el-button type="primary" @click="submitDeleteGroup()">确认删除</el-button>
                  </div>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </div>

  </hs-layout_auto>
</template>

<script>
  export default {
    data() {
      return {
        selectList: '',
        pages: 0,
        page2: 0,
        page3: 0,
        istableData3: 0,
        add_form: {
          'permission_group': '',
          'user': []
        },
        del_form: {
          'permission_group': [],
          'user': ''
        },
        tableData1: [],
        tableData2: [],
        tableData3: [],
        tableData4: [],
        multipleSelection: [],
        multipleSelectionId: []
      }
    },
    // activated: function () {
    //   this.get_all_list();
    // },
    activated: function () {
      this.get_all_list();
    },
    methods: {
      get_all_list() {
        this.$http.get(this.passport + 'list').then((resp) => {
          // console.log('this resp', resp.data)
          this.tableData1 = resp.data.all_user;
          this.tableData2 = resp.data.permission_data;
          this.tableData4 = resp.data.user_group;
          this.pages = this.tableData1.length;
          this.page2 = this.tableData2.length;
          // console.log(this.tableData4)
        }).catch((error) => {
          this.tableData1 = 'error'
          // console.log(this.tableData1)
        })
      },
      // 拿到了选中的行啦
      // handleCheckedCitiesChange(row) {
      //   this.selectList = row;
      //   console.log('selectList', this.selectList);
      // },
      handleSelectionChange(val) {
        if (this.add_form.permission_group.length === 0) {
          this.$alert('请选择权限组。。')
          this.toggleSelection();
        } else {
          this.multipleSelection = val;
        }
        // console.log('handleSelectionChange', this.multipleSelection)
      },
      toggleSelection() {
        this.$refs.multipleTable.clearSelection();
      },
      toggleSelections() {
        this.$refs.multipleTables.clearSelection();
      },
      // 组合到add_from 里提交
      submitSelection() {
        // console.log(this.multipleSelection)
        for (let i in this.multipleSelection) {
          this.add_form['user'].push(this.multipleSelection[i]['id'])
        }
        for (let t in this.tableData2) {
          // console.log(this.tableData2[t]['name'])
          if (this.add_form['permission_group'] === this.tableData2[t]['name']) {
            this.add_form['permission_group'] = this.tableData2[t]['id'];
          }
        }
        console.log('add_form', this.add_form);
        this.$http.post(this.passport + 'user_add_group/', this.add_form).then((resp) => {
          this.toggleSelection();
          this.add_form['permission_group'] = '';
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '添加成功',
              type: 'success'
            })
          }
          console.log(resp.data.msg)
        }).catch((error) => {
          this.$alert(error.data.msg)
        })
        // this.toggleSelection();
      },
      deleteSelectionChange(val) {
        if (this.del_form.user.length === 0) {
          this.$alert('请选择用户。。')
          this.toggleSelection();
        } else {
          this.multipleSelectionId = val;
          console.log('multipleSelectionId', this.multipleSelectionId)
        }
      },
      submitDelete() {
        for (let i in this.multipleSelectionId) {
          this.del_form['permission_group'].push(this.multipleSelectionId[i]['id'])
        }
        for (let t in this.tableData1) {
          // console.log(this.tableData2[t]['name'])
          if (this.del_form['user'] === this.tableData1[t]['username']) {
            this.del_form['user'] = this.tableData1[t]['id'];
          }
        }
        console.log('del_form', this.del_form);
        this.$http.post(this.passport + 'user_del_group/', this.del_form).then((resp) => {

          this.del_form['user'] = '';
          this.istableData3 = 0;
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '删除成功',
              type: 'success'
            })
          }
          this.toggleSelections();
          console.log(resp.data.msg)
        }).catch((error) => {
          this.$alert(error.data.msg)
        })
      },
      submitDeleteGroup() {
        for (let i in this.multipleSelectionId) {
          this.del_form['permission_group'].push(this.multipleSelectionId[i]['group_id'])
        }
        for (let t in this.tableData1) {
          // console.log(this.tableData2[t]['name'])
          if (this.del_form['user'] === this.tableData1[t]['username']) {
            this.del_form['user'] = this.tableData1[t]['id'];
          }
        }
        console.log('del_form', this.del_form);
        this.$http.post(this.passport + 'user_del_group/', this.del_form).then((resp) => {
          this.toggleSelections();
          this.del_form['user'] = '';
          this.istableData3 = 0;
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '删除成功',
              type: 'success'
            })
          }
          console.log(resp.data.msg);
          this.get_all_list();
        }).catch((error) => {
          this.$alert(error.data.msg)
        })
      },
      isGroups() {
        this.istableData3 = 1;
        for (let t in this.tableData1) {
          // console.log(this.tableData2[t]['name'])
          if (this.del_form['user'] === this.tableData1[t]['username']) {
            var user_id = this.tableData1[t]['id'];
          }
        }
        console.log('isGroups', this.del_form);
        this.$http.get(this.passport + 'is_group/', {params: user_id}).then((resp) => {
          this.tableData3 = resp.data.data;
          this.page3 = resp.data.data.length;
          // console.log('this.tableData3', this.tableData3)
        }).catch((error) => {
          // this.$alert(error.data.mag)
        })
      },
      handleClick() {
        console.log('handleClick')
        // this.get_all_list();
      }
    }
  }
</script>

<style>

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }

  .el-pager li.active {
    border-color: #149C4C;
    background-color: #149C4C;
  }
</style>
