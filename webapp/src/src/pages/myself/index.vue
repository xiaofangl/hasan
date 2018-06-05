<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class" style="background-color: white">
        <el-card class="box-card">
          <el-tabs type="border-card">
            <el-tab-pane label="我的权限">
              <el-collapse v-model="activeNames">
                <el-collapse-item title="已有权限" name="1">
                  <div style="font-weight: 700; font-size: 16px;">用户： {{username}}</div>
                  <!--<div>{{groups}}</div>-->
                  <el-table :data="groups" tooltip-effect="dark" style="width: 100%">
                    <el-table-column width="55">
                    </el-table-column>
                    <el-table-column label="ID" width="120" prop="group_id">
                    </el-table-column>
                    <el-table-column prop="group__groupextend__be_app" label="APP" width="120">
                    </el-table-column>
                    <el-table-column prop="group__name" label="权限组" show-overflow-tooltip>
                    </el-table-column>
                  </el-table>
                </el-collapse-item>
                <el-collapse-item title="申请权限" name="2">
                  <el-form ref="applyPermission" label-width="80px" :rules="applyPermissions">
                    <el-form-item label="模块" prop="app">
                      <el-select v-model="applyPermission.app" placeholder="请选择需要申请权限的APP">
                        <el-option :value="item" :key="item" v-for="item in result">{{item}}</el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="内容" prop="text">
                      <el-input type="textarea" :rows="2" placeholder="请输入具体操作的描述，如：申请操作DNS权限，新增解析记录等"
                                v-model="applyPermission.text">
                      </el-input>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="submitApply()">提交申请</el-button>
                    </el-form-item>
                  </el-form>

                </el-collapse-item>
              </el-collapse>
            </el-tab-pane>
            <el-tab-pane label="我的操作">

            </el-tab-pane>
            <el-tab-pane label="数据库管理">
              <el-collapse v-model="sqlModels">
                <el-collapse-item title="已有dbmain账号" name="1">
                  <el-row>
                    <el-col :span="12" >
                      <a target="_blank" :href="dbmain" class="aClass bigFont">
                        去往dbmain数据库管理平台
                      </a>
                    </el-col>
                    <el-col :span="12" class="textClass">
                      <span >
                         <p class="textLine">关于dbmain</p>
                        <p class="textLine">dbmain是数据库SQL审核平台</p>
                        <p class="textLine">dbamin 使用独立账号管理，如无dbmain账号请在下面申请</p>
                      </span>
                    </el-col>
                  </el-row>

                </el-collapse-item>
                <el-collapse-item title="申请dbmain账号" name="2">

                  <el-form ref="dbmainForm" label-width="80px">
                    <el-form-item label="用户">{{username}}</el-form-item>
                    <el-form-item label="内容" prop="text">
                      <el-input type="textarea" :rows="2" placeholder="请输入申请内容，如 申请开通的用户、操作数据库、表的权限等"
                                v-model="dbmainForm.text">
                      </el-input>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="dbmainApply()">提交申请</el-button>
                    </el-form-item>
                  </el-form>

                </el-collapse-item>
              </el-collapse>
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
        activeNames: ['1', '2'],
        sqlModels: ['1', '2'],
        dbmain: 'http://dbmain.huashenghaoche.work',
        username: '',
        groups: '',
        result: [],
        tableData2: '',
        allApps: [],
        dbmainForm: {
          'user': '',
          'text': ''
        },
        applyPermission: {
          'user': '',
          'text': '',
          'app': ''
        },
        applyPermissions: {
          app: [{ required: true, message: '请选择申请哪个模块应用的权限', trigger: 'change' }],
          text: [{ required: true, message: '请输入尽量详细的权限描述', trigger: 'blur' }]
        }
      }
    },
    created: function () {
      if (this.$route.params.hasOwnProperty('h')) {
        this.h = this.$route.params.h
      }
    },
    activated: function () {
      this.getUserInfo();

    },
    methods: {
      // handThis () {
      //   window.location.href = 'dbmain.huashenghaoche.work';
      // },
      checkInput() {
        // let numbers = /^1\d{10}$/;
        if (this.dbmainForm.text.length === 0) {
          this.$alert('请输入申请信息!');
          return false
        }
        return true
      },
      getUserInfo() {
        this.username = window.localStorage.getItem('username');
        this.$http.get(this.passport + 'user_group/').then((resp) => {
          this.groups = resp.data.data;
        }).catch((error) => {
          console.log(error)
        })
        this.$http.get(this.passport + 'list').then((resp) => {
          this.tableData2 = resp.data.permission_data;
          // console.log(this.tableData2);
          for (let item in this.tableData2) {
            this.allApps.push(this.tableData2[item]['groupextend__be_app'])
          }
          let len = this.allApps.length;
          for (let i = 0; i < len; i++) {
            for (let j = i + 1; j < len; j++) {
              if (this.allApps[i] === this.allApps[j]) {
                j = ++i;
              }
            }
            this.result.push(this.allApps[i]);
          }

          // console.log(' this.allApps', this.allApps)
        }).catch((error) => {
          console.log(error)
        })
      },
      submitApply() {
        this.applyPermission.user = window.localStorage.getItem('username');
        console.log('applyPermission', this.applyPermission);
        this.$http.post(this.passport + 'apply_permission/', this.applyPermission).then((resp) => {
          console.log(resp);
          this.$notify({
            title: '成功',
            message: '权限申请成功',
            type: 'success'
          })
          if (this.h) {
            this.$router.go(-1)
          } else {
            window.location = '/myself';
          }
        }).catch((error) => {
          console.log(error);
          this.$notify({
            title: '失败',
            message: '权限申请失败',
            type: 'success'
          })
        })
      },
      dbmainApply() {
        if (this.checkInput()) {
          // 给DBA发邮件，后端send mail api
          this.dbmainForm.user = window.localStorage.getItem('username');
          console.log('dbmainForm', this.dbmainForm);
          this.$http.post(this.passport + 'apply_dbmain/', this.dbmainForm).then((resp) => {
            console.log(resp);
            this.$notify({
              title: '成功',
              message: '申请成功',
              type: 'success'
            })
            if (this.h) {
              this.$router.go(-1)
            } else {
              window.location = '/myself';
            }
          }).catch((error) => {
            console.log(error);
            this.$notify({
              title: '失败',
              message: '申请失败',
              type: 'success'
            })
          })
        }
      }
    }
  }
</script>
<style>
  .text {
    font-size: 14px;
  }

  .item {
    padding: 18px 0;
  }

  .box-card {
    width: 100%;
  }

  .itemclass {
    padding: 25px 50px;
  }

  .tclass {
    color: rgb(20, 156, 76);
    font-weight: 700;
    font-size: 16px;
  }

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }
  .textClass {
    background-color: white;
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }
  .textLine {
    margin-left: 15px;
  }
  .aClass {
    display: flex;
    align-items: center;
  }
  .bigFont {
    font-weight: 700;
    font-size: 16px;
    color: #1F3D2E
  }
</style>
