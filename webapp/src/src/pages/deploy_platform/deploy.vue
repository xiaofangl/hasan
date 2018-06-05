<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class" style="background-color: white">
        <el-card class="box-card">
          <el-tabs type="border-card">
            <el-tab-pane label="DEPLOY">
              <div style="margin-top: 15px">
                <template v-if="isdeploy_admin">
                  <router-link :to="{name: '012-1'}">
                    <el-button class="" type="primary">+ 新建项目</el-button>
                  </router-link>
                </template>
                <template v-else>
                  <el-button class="" type="primary" @click="no_permission = true">+ 新建项目</el-button>
                </template>
                <div style="margin-bottom: 35px; width: 30%; float: right;">
                  <el-input placeholder="请输入项目名称" v-model.trim="input3" @keyup.enter.native="EnterName(input3)">
                    <template slot="prepend">项目名称搜索</template>
                  </el-input>
                </div>
              </div>
              <el-table :data="resForm" style="width: 100%" height="650"
                        :default-sort="{prop: 'id', order: 'descending'}">
                <el-table-column prop="id" label="ID" sortable>
                </el-table-column>
                <el-table-column prop="name" label="项目名称">
                </el-table-column>
                <el-table-column prop="type" label="语言类型">
                </el-table-column>
                <el-table-column prop="" label="线上版本">
                </el-table-column>
                <el-table-column prop="describe" label="描述">
                </el-table-column>
                <el-table-column prop="server_port" label="端口">
                </el-table-column>
                <el-table-column prop="created" label="创建时间" sortable>
                </el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="clickDeploy(scope.row)">发布</el-button>
                    <template v-if="isdeploy_admin">
                      <router-link :to="{name: '012', params:{id:scope.row['id']}}">
                        <el-button size="mini" type="warning">Manage</el-button>
                      </router-link>
                    </template>
                    <template v-else><el-button size="mini" type="warning" @click="no_permission = true">Manage</el-button></template>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="OTHER">
              <div style="margin-top: 15px">
                <template v-if="isdeploy_admin">
                  <router-link :to="{name: ''}">
                    <el-button class="" type="primary" disabled>+ 日志</el-button>
                  </router-link>
                </template>
                <template v-else>
                  <el-button class="" type="primary" @click="no_permission = true" disabled>+ 日志</el-button>
                </template>
                <div style="margin-bottom: 35px; width: 30%; float: right;">
                  <el-input placeholder="请输入项目名称" v-model.trim="input3" disabled>
                    <template slot="prepend">日志项目名称搜索</template>
                  </el-input>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </div>

    <el-dialog title="发布" :visible.sync="dialogFormVisible">
      <el-col slot="title" class="dialog_title">
        <span>发布项目：{{ form.name }}</span>
      </el-col>
      <el-form :model="form">
        <el-form-item label="代码版本" :label-width="formLabelWidth" :rules="[{ required: true, message: '代码版本不能为空'}]">
          <el-select v-model="form.branch" placeholder="请选择代码版本">
            <el-option :label="item" :value="item" v-for="item in packageList">{{item}}</el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="部署路径" :label-width="formLabelWidth">
          {{resForms['server_path']}}
        </el-form-item>
        <el-form-item label="主机地址" :label-width="formLabelWidth">
          <!--<span v-for="item in resHosts">{{item.hostname}}</span>-->
          <el-button size="mini" type="info" v-for="item in resHosts">{{item.hostname}}</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitDeploy">立即发布</el-button>
      </div>
    </el-dialog>

    <el-dialog title="结果" :visible.sync="enable_add">
      <el-col slot="title" class="dialog_title">
        <span>发布项目：{{ form.name }}</span>
      </el-col>
      <span v-for="item in res_data['data']">
          <p style="text-align: center">{{item}}</p>
        </span>
      <el-col>

      </el-col>
      <div slot="footer" class="dialog-footer">
        <el-button @click="enable_add=false" type="primary">关闭</el-button>
      </div>
    </el-dialog>

    <el-dialog title="权限" :visible.sync="no_permission">
      <el-col slot="title" class="dialog_title">
        <span>没有权限</span>
      </el-col>

      <el-col>
        <span>您没有权限，请联系 业务运维人员 或者为ops运维组发邮件。。。</span>
      </el-col>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="toMyself">去申请</el-button>
        <el-button @click="no_permission=false" type="primary">关闭</el-button>
      </div>
    </el-dialog>

  </hs-layout_auto>
</template>
<script>
  export default {
    data() {
      return {
        isdeploy_admin: false,
        no_permission: false,
        formLabelWidth: '98px',
        dialogFormVisible: false,
        packForm: '',
        packageList: '',
        packRes: {},
        form: {
          id: '',
          name: '',
          branch: '',
          host: '',
          server_path: ''
        },
        user_group: '',
        resHosts: '',
        item_id: '',
        input3: '',
        tmp: [],
        activeNames: ['1', '2'],
        projectForm: {
          'name': '',
          'type': '',
          'repository': '',
          'branches': '',
          'repos_user': '',
          'builder': '',
          'build_info_pom': '',
          'bulid_info_param': '',
          'project_env': [],
          'dev_address': '',
          'pro_address': '',
          'describe': '创建用户'

        },
        resForm: '',
        resForms: '',
        enable_add: false,
        res_data: ''
      };
    },
    created: function () {
      this.bus.$on('isdeploy_admin', function (val) {
        console.log('val', val);
        this.isdeploy_admin = val;
      }.bind(this));
    },
    activated: function () {
      this.get_all_list();
      console.log(this.isdeploy_admin)
    },
    methods: {
      get_all_list() {
        console.log(this.deploy_api + 'list/')
        this.$http.get(this.deploy_api + 'list/').then((resp) => {
          // console.log('this resp', moment(resp.data.data.created).format('YYYY-MM-DD'))
          this.resForm = resp.data.data;
          // this.resForm = moment(this.resForm.created).format('YYYY-MM-DD');
          // console.log('resform', this.resForm)
        }).catch((error) => {
          console.log(error)
        });
      },
      clickDeploy(row) {
        // console.log('clickDeploy', row);
        this.form.name = row['name'];
        // this.item_id = row['id'];
        this.form.id = row['id'];
        this.$http.get(this.deploy_api + 'mod_item/', {params: this.form.id}).then((resp) => {
          console.log('this resp', resp.data)
          this.dialogFormVisible = !this.dialogFormVisible;
          this.resForms = resp.data.data[0];
          // console.log('clickdeploy', this.resForms, row['id']);
          this.$http.post(this.deploy_api + 'package_list/', this.resForms).then((resp) => {
            // console.log(resp.data);
            // this.tmp = resp.data;
            this.packageList = resp.data.data;
            this.packRes['project_url'] = resp.data.url;
          }).catch((error) => {
            console.log(error)
          })
          // this.resUsers = resp.data.users;
          if (resp.data.hosts) {
            this.resHosts = resp.data.hosts;
            this.form.host = resp.data.hosts;
            this.form.server_path = resp.data.data['server_path'];
          } else {
            this.dialogFormVisible = !this.dialogFormVisible;
            this.$alert('This Project Not Host, Please Settings in Manage...')
          }
          // console.log('resresHostsform', this.resHosts)
        }).catch((error) => {
          this.resForm = 'error'
          console.log(error)
        });
      },
      submitDeploy() {
        // console.log('submitDeploy', this.form);
        if (this.form.branch.length === 0) {
          this.$alert('Please Choose Deploy Package...')
        } else {
          for (let n in this.form.host) {
            this.tmp.push(this.form.host[n]['hostname'])
          }
          ;
          this.packRes['id'] = this.resForms.id;
          this.packRes['package_url'] = this.packRes['project_url'] + this.form.branch;
          this.packRes['host_list'] = this.tmp;
          this.packRes['client_path'] = this.resForms.server_path;
          this.packRes['client_port'] = this.resForms.server_port;
          this.packRes['project_name'] = this.resForms.name;
          this.packRes['package_name'] = this.form.branch;
          // console.log('deployForm', this.packRes);
          this.$http.post(this.deploy_api + 'run_deploy/', this.packRes).then((resp) => {
            this.packRes['host_list'] = [];
            // console.log('submitDeploy', resp.data);
            if (resp.data.status) {
              this.res_data = resp.data;
              this.dialogFormVisible = false;
              this.enable_add = true;
            } else {
              this.dialogFormVisible = !this.dialogFormVisible;
              this.$alert(resp.data.msg);
            }

          }).catch((error) => {
            console.log(error);
            this.packRes['host_list'] = [];
            this.$alert(error)
            // this.$alert('My dear baby, back-end PythonAPI haven\'t written yet... ')
          })
        }
      },
      toMyself() {
        // console.log(window.localStorage.getItem('permission');
        window.location = '/myself';
      },
      EnterName(input) {
        console.log('input', input);
        this.$http.get(this.deploy_api + 'list/', {params: input}).then((resp) => {
          // console.log(resp.data);
          this.resForm = resp.data.data;
        }).catch((error) => {
          console.log(error)
        })
      }
    }
  }
</script>
<style>
  .v-modal {
    display: none;
  }

  .el-select {
    width: 81%;
  }

  .rightbutton {
    margin-bottom: 15px;
    /*border: 1px solid rgb(191, 217, 204);*/
    /*background-color: #149C4C;*/
    /*color: white;*/
  }

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }

  .el-input-group__append, .el-input-group__prepend {
    background-color: #149C4C;
    color: white;
    border: #149c4c;
  }

  .el-message-box {
    border: 1px solid rgb(191, 217, 204);
    color: #ff4949;
  }
</style>
