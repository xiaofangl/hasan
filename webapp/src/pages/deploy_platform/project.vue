<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class">
        <el-card class="box-card" style="width: 100%">
          <div slot="header" class="clearfix">
              <span style="color: #149C4C; font-weight: 700; font-size: 16px">
                {{resForm[0]['name']}}
              </span>
            <span>
                <router-link class="right" :to="{name: '013'}">
                        <el-button class="rightbutton" type="primary" @click="">发布管理</el-button>
                </router-link>

              </span>
          </div>
          <div class="textClass">
            <dl>
              <dt>开发语言：</dt>
              <dd>{{resForm[0]['type']}}</dd>
            </dl>
            <dl>
              <dt>gitlab地址：</dt>
              <dd>{{resForm[0]['repository']}}</dd>
            </dl>
            <dl>
              <dt>部署路径：</dt>
              <dd>{{resForm[0]['server_path']}}</dd>
            </dl>
            <dl>
              <dt>创建时间：</dt>
              <dd>{{resForm[0]['created']}}</dd>
            </dl>
            <dl>
              <dt>软件下载路径：</dt>
              <dd>{{resForm[0]['download_path']}}</dd>
            </dl>
          </div>
          <div class="md">发布人员列表</div>
          <el-row>
            <el-col :span="12">
              <el-select v-model.trim="modForm.user" placeholder="添加发布人员" style="width: 100%" @change="userExist">
                <el-option :value="item.username" :key="item.id" v-for="item in tableData1">{{item.username}}
                </el-option>

              </el-select>
            </el-col>
            <el-col :span="8">
              <el-button type="primary" @click="addUsers">确认添加</el-button>
              <el-button type="primary" disabled>批量添加</el-button>
            </el-col>
          </el-row>
          <el-table :data="resUsers" border style="width: 100%">
            <el-table-column prop="user__username" label="Name"></el-table-column>
            <el-table-column prop="user__email" label="email"></el-table-column>
            <el-table-column prop="title" label="title"></el-table-column>
            <el-table-column prop="status" label="status"></el-table-column>
            <el-table-column prop="Action" label="Action">
              <template slot-scope="scope">
                  <el-button size="mini" type="danger" @click="deleteUser(scope.row)">DELETE</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="md">主机管理</div>
          <el-tabs type="border-card">
            <el-tab-pane label="主机列表">
              <el-row>
                <el-col :span="12">
                  <el-input placeholder="请输入内容" v-model.trim="modForm.host" @blur="hostExist"></el-input>
                </el-col>
                <el-col :span="8">
                  <el-button type="primary" @click="addHost">添加主机</el-button>
                  <el-button type="primary" disabled>批量添加</el-button>
                </el-col>
              </el-row>
              <el-table :data="resHosts" border style="width: 100%">
            <el-table-column prop="hostname" label="主机名"></el-table-column>
            <el-table-column prop="created" label="创建时间"></el-table-column>
            <!--<el-table-column prop="title" label="管理员"></el-table-column>-->
            <el-table-column prop="Action" label="Action">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="deleteHost(scope.row)">DELETE</el-button>
              </template>
            </el-table-column>
          </el-table>
            </el-tab-pane>
            <el-tab-pane label="other"></el-tab-pane>
          </el-tabs>
          <div class="md">删除项目</div>
          <el-button type="danger" @click="DeleteItem">DELETE</el-button>
        </el-card>
      </div>
    </div>

  </hs-layout_auto>
</template>

<script>
  export default {
    data () {
      return {
        modForm: {
          'id': '',
          'user': '',
          'user_id': '',
          'host': '',
          'hostname': ''
        },
        tableData1: [],
        resForm: '',
        resUsers: '',
        resHosts: '',
        input3: '',
        enable_add: false,
        item_id: ''
      };
    },
    activated: function () {
      if (this.$route.params.hasOwnProperty('h')) {
        this.h = this.$route.params.h
      };
      this.get_all_list();
    },
    methods: {
      get_all_list() {
        // console.log(this.deploy_api + 'list/')
        console.log('project', this.$route.params.id)
        if (this.$route.params.id) {
          this.item_id = this.$route.params.id;
        }
        this.$http.get(this.deploy_api + 'mod_item/', {params: this.item_id}).then((resp) => {
          console.log('this resp', resp.data)
          this.resForm = resp.data.data;
          this.resUsers = resp.data.users;
          this.resHosts = resp.data.hosts;
          // console.log('resform', this.resForm)
        }).catch((error) => {
          this.resForm = 'error'
          console.log(this.resForm)
        });
        this.$http.get(this.passport + 'list').then((resp) => {
          // console.log('this resp', resp.data)
          this.tableData1 = resp.data.all_user
        }).catch((error) => {
          console.log(error)
        })
      },
      userExist () {
        // console.log('userexist', this.modForm.user, this.resUsers);
        for (let t in this.resUsers) {
          // console.log(this.resUsers[t]);
          // this.modForm['user'] = '';
          if (this.modForm.user === this.resUsers[t]['user__username']) {
            this.$alert('This User is Exist, Please Choose Again...');
            this.modForm.user = '';
          };
        }
      },
      hostExist () {
        // console.log('userexist', this.modForm.host, this.resHosts);
        for (let t in this.resHosts) {
          if (this.modForm.host === this.resHosts[t]['hostname']) {
            this.$alert('This Host is Exist, Please Input Again...');
            this.modForm.host = '';
          }
        }
      },
      addUsers () {
        if (this.modForm.user.length === 0) {
          this.$alert('Select Not Empty...')
        } else {
          for (let t in this.tableData1) {
            // console.log(this.tableData2[t]['name'])
            if (this.modForm['user'] === this.tableData1[t]['username']) {
              this.modForm['user_id'] = this.tableData1[t]['id'];
            }
          };
          this.modForm['host'] = '';
          this.modForm['id'] = this.resForm[0]['id'];
          console.log('addUsers', this.modForm);
          this.$http.post(this.deploy_api + 'mod_item/', this.modForm).then((resp) => {
            if (resp.data.status) {
              this.$notify({
                title: '成功',
                message: '信息已提交',
                type: 'success'
              });
              this.modForm['user_id'] = '';
              this.get_all_list();
            } else {
              this.$alert(resp.data.msg)
            }
          }).catch((error) => {
            console.log(error)
          })
        }
      },
      deleteUser (row) {
        console.log('deleteUser', row['user__username']);
        this.modForm['host'] = '';
        for (let t in this.tableData1) {
          // console.log(this.tableData2[t]['name'])
          if (row['user__username'] === this.tableData1[t]['username']) {
            this.modForm['user_id'] = this.tableData1[t]['id'];
          }
        };
        this.modForm['id'] = this.resForm[0]['id'];
        console.log(this.modForm);
        this.$http.put(this.deploy_api + 'mod_item/', this.modForm).then((resp) => {
          if (resp.data.status) {
            this.modForm.user_id = '';
            this.get_all_list();
          } else {
            this.$alert(resp.data.msg);
          }
        }).catch((error) => {
          console.log(error)
        })

      },
      addHost () {
        this.modForm['user_id'] = '';
        this.modForm['id'] = this.resForm[0]['id'];
        // console.log('addhost', this.modForm);
        if (this.modForm.host.length === 0) {
          this.$alert('Input Not Empty...')
        } else {
          this.$http.post(this.deploy_api + 'mod_item/', this.modForm).then((resp) => {
            if (resp.data.status) {
              this.$notify({
                title: '成功',
                message: '信息已提交',
                type: 'success'
              });
              this.modForm['host'] = '';
              this.get_all_list();
            } else {
              this.$alert(resp.data.msg)
            }
          }).catch((error) => {
            console.log(error)
          })
        }
      },
      deleteHost (row) {
        this.modForm['user_id'] = '';
        this.modForm['hostname'] = row['hostname'];
        this.modForm['id'] = this.resForm[0]['id'];
        console.log('deleteHost', row, this.modForm);
        this.$http.put(this.deploy_api + 'mod_item/', this.modForm).then((resp) => {
          if (resp.data.status) {
            this.modForm.host = '';
            this.get_all_list();
          } else {
            this.$alert(resp.data.msg)
          }
        }).catch((error) => {
          console.log(error)
        })
      },
      DeleteItem() {
        console.log('delete', this.resForm[0]['id']);
        // if (this.h) {
        //   this.$router.go(+1)
        // } else {
        //   window.location = '/deploy_platform/deploy';
        // };
        this.modForm['id'] = this.resForm[0]['id'];
        this.$http.delete(this.deploy_api + 'del_item/', {params: this.item_id}).then((resp) => {
          if (resp.data.status) {
            if (this.h) {
              this.$router.go(+1)
            } else {
              window.location = '/deploy_platform/deploy';
            };
            this.modForm['host'] = '';
          } else {
            this.$alert(resp.data.msg)
          }
        }).catch((error) => {
          console.log(error)
        })
      }
    }
  }
</script>
<style>
  dl{
    padding:5px;
    margin:3px;
    clear:left;

  }
  dl dt {
    float:left;
  }
  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }
  .rightbutton {
    float: right;
    /*border: 1px solid rgb(191, 217, 204);*/
    /*background-color: #149C4C;*/
    /*color: white;*/
  }
  .md{
    color: #149C4C;
    font-weight: 700;
    font-size: 16px;
    border-bottom: 1px solid rgb(191, 217, 204);
    padding-top: 15px;
    padding-bottom: 15px;
    margin-bottom: 15px;
  }
  .textClass {
    background-color: white;
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
    padding: 15px;
  }
</style>
