<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class" v-for="item in res_data">

        <el-card class="box-card">
          <div slot="header" class="clearfix">
                <span style="color: #149C4C; font-weight: 700; font-size: 16px">
                  {{ item[0]}}
                </span>
            <span>
                  <el-button style="float: right; padding: 3px 0" type="text"
                             @click="add_item(item[0])">添加解析</el-button>
                </span>

          </div>
          <div class="text item">
            <el-table :data="item[1]" style="width: 100%" height="250">
              <el-table-column prop="id" label="记录ID">
              </el-table-column>
              <el-table-column prop="type" label="记录类型">
              </el-table-column>
              <el-table-column prop="host" label="主机记录">
              </el-table-column>
              <el-table-column prop="ns_path" label="解析线路">
              </el-table-column>
              <el-table-column prop="value" label="记录值">
              </el-table-column>
              <el-table-column prop="mx" label="MX优先级">
              </el-table-column>
              <el-table-column prop="ttl" label="TTL值">
              </el-table-column>
              <el-table-column prop="file_name" label="文件">
              </el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>


      </div>
    </div>

    <el-dialog v-model="enable_add" :visible.sync="enable_add">
      <el-col slot="title" class="dialog_title">
        <span>添加解析到：{{ add_recods.file_name }}</span>
      </el-col>
      <el-form :model="add_recods" ref="add_recods" style="width: 90%;" :rules="rules">
        <el-form-item label="记录类型：" :label-width="formLabelWidth" prop="type">
          <el-select v-model="add_recods.type" placeholder="请选择记录类型">
            <el-option label="A" value="A"></el-option>
            <el-option label="CNAME" value="CNAME"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="主机记录：" :label-width="formLabelWidth" prop="value">
          <el-input type="text" v-model.trim="add_recods.value"
                    placeholder="输入主机记录如：1.1.1.1"></el-input>
        </el-form-item>

        <!--<el-form-item label="解析线路：" :label-width="formLabelWidth" >-->
        <!--<el-select v-model="add_recods.ns_path" placeholder="请选择解析线路">-->
        <!--<el-option label="默认" value="-"></el-option>-->
        <!--</el-select>-->
        <!--</el-form-item>-->
        <el-form-item label="记录值：" :label-width="formLabelWidth" prop="host">
          <el-input type="text" v-model.trim="add_recods.host"
                    placeholder="输入记录值"></el-input>
        </el-form-item>

        <!--<el-form-item label="TTL值：" :label-width="formLabelWidth" >-->
        <!--<el-select v-model="add_recods.ttl" placeholder="请选择解析线路">-->
        <!--<el-option label="10分钟" value="10"></el-option>-->
        <!--</el-select>-->
        <!--</el-form-item>-->

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="subRecode('add_recods')" type="success">立即提交</el-button>
        <el-button @click="resetRecode('add_recods')">重置</el-button>
      </div>
    </el-dialog>

    <el-dialog title="提示" :visible.sync="dialogVisible" width="35%">
      <dl>
        <span>{{one_row.file_name}} : &nbsp</span>
        <span>{{one_row.type}}</span>
        <span>{{one_row.host}}</span>
        <span>{{one_row.value}}</span>
      </dl>
      <dl>确定要删除这条记录吗？</dl>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleRecode()">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="警告" :visible.sync="outerVisible">
        <span style="color: #149C4C; font-weight: 700; font-size: 16px">
                {{permissionMsg}}
        </span>

      <!--<el-dialog width="50%" title="提示" :visible.sync="innerVisible" append-to-body>-->
      <!--申请操作权限。。-->
      <!--</el-dialog>-->
      <div slot="footer" class="dialog-footer">
        <el-button @click="outerVisible = false">取 消</el-button>
        <!--<router-link :to="{name: '009'}">-->
        <el-button type="primary" @click="toMyself">去申请</el-button>
        <!--</router-link>-->

      </div>
    </el-dialog>

  </hs-layout_auto>
</template>
<script>
  export default {
    data() {
      return {
        permissionMsg: '',
        outerVisible: false,
        enable_add: false,
        dialogVisible: false,
        formLabelWidth: '108px',
        editableTabsValue: '2',
        editableTabs: [{
          title: 'Tab 1',
          name: '1',
          content: 'Tab 1 content'
        }, {
          title: 'Tab 2',
          name: '2',
          content: 'Tab 2 content'
        }],
        tabIndex: 2,
        res_data: {},
        file_name: '',
        add_recods: {
          'file_name': '',
          'type': '',
          'host': '',
//          'ns_path': '-',
          'value': ''
//          'ttl': ''
        },
        one_row: {
          'file_name': '',
          'type': '',
          'host': '',
//          'ns_path': '-',
          'value': ''
//          'ttl': ''
        },
        rules: {
          type: [{required: true, message: '请选择记录类型', trigger: 'change'}],
          value: [{required: true, message: '输入主机记录', trigger: 'blur'}],
          host: [{required: true, message: '输入记录值', trigger: 'blur'}]
        }
      }
    },
    activated: function () {
      this.get_all_list();
    },
    methods: {
      add_item(file) {
        this.enable_add = !this.enable_add;
        this.add_recods.file_name = file;
        console.log('file', this.add_recods.file_name, this.enable_add)
      },
      subRecode(file) {
        this.$refs[file].validate((vaild) => {
          if (vaild) {
            console.log('add_info', this.add_recods)
            this.$http.post(this.dns_api + 'add_item/', this.add_recods).then((resp) => {
              this.permissionControl(resp);
              this.enable_add = !this.enable_add;
              this.$notify({
                title: '成功',
                message: '信息已提交',
                type: 'success'
              });
              this.get_all_list();
              this.add_recods.file_name = '';
              this.add_recods.value = '';
              this.add_recods.host = '';
              this.add_recods.type = ''
            }).catch((error) => {
              this.$notify.error({
                title: '错误',
                message: '信息提交失败'
              });
            })

          } else {
            return false;
          }
        })
      },
      permissionControl(resp) {
        if (resp.data.code === '21') {
          window.localStorage.setItem('permission', resp.data.data);
          this.permissionMsg = resp.data.msg;
          this.outerVisible = true;
          let username = window.localStorage.getItem('permission');
          console.log(username)
          // this.$alert(resp.data.msg + '请先在 个人中心 申请：' + resp.data.data + ' 组权限')
        }
      },
      toMyself() {
        // console.log(window.localStorage.getItem('permission');
        this.outerVisible = !this.outerVisible;
        window.location = '/myself';
      },
      // handleTabsEdit(targetName, action) {
      //   if (action === 'add') {
      //     let newTabName = ++this.tabIndex + '';
      //     this.editableTabs.push({
      //       title: 'New Tab',
      //       name: newTabName,
      //       content: 'New Tab content'
      //     });
      //     this.editableTabsValue = newTabName;
      //   }
      //   if (action === 'remove') {
      //     let tabs = this.editableTabs;
      //     let activeName = this.editableTabsValue;
      //     if (activeName === targetName) {
      //       tabs.forEach((tab, index) => {
      //         if (tab.name === targetName) {
      //           let nextTab = tabs[index + 1] || tabs[index - 1];
      //           if (nextTab) {
      //             activeName = nextTab.name;
      //           }
      //         }
      //       });
      //     }
      //
      //     this.editableTabsValue = activeName;
      //     this.editableTabs = tabs.filter(tab => tab.name !== targetName);
      //   }
      // },
      get_all_list() {
        console.log(this.dns_api + 'list')
        this.$http.get(this.dns_api + 'list').then((resp) => {
//                      console.log('this resp', resp.data)
//           this.permissionControl(resp);
          this.res_data = resp.data;
        }).catch((error) => {
          this.res_data = 'error'
          console.log(this.res_data)
        })
      },
      handleClick(one_row) {
        this.dialogVisible = !this.dialogVisible;
        this.one_row = one_row;
        // console.log('row:', one_row, typeof(one_row));
      },
      handleRecode() {
        this.dialogVisible = !this.dialogVisible;
        this.$http.post(this.dns_api + 'mod_item/', this.one_row).then((resp) => {
          this.permissionControl(resp);
          this.$notify({
            title: '成功',
            message: '删除成功',
            type: 'success'
          });
          this.get_all_list();
        }).catch((error) => {
          this.$notify.error({
            title: '错误',
            message: '删除失败'
          });
        })
      },
      resetRecode(formName) {
        this.$refs[formName].resetFields();
        console.log('this reset', formName)
      }
    }
  }
</script>
<style>
  .el-dialog {
    width: 50%;
  }

  .v-modal {
    display: none;
  }

  .el-tabs__new-tab {
    float: left;
  }

  .el-tabs__content {
    padding-left: 20px;
  }

  .el-form {
    width: 80%;
  }

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }
</style>
