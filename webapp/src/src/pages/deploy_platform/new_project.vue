<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class"></div>

      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
              <span style="color: #149C4C; font-weight: 700; font-size: 16px">
                创建项目
              </span>
          <span>
                <router-link class="right" :to="{name: '013'}">
                        <el-button class="rightbutton" type="primary" @click="">发布管理</el-button>
                </router-link>

              </span>
        </div>
        <el-tabs type="border-card">
          <el-tab-pane label="PROJECT">
            <el-form :model="projectForm" ref="projectForm" label-width="140px" :rules="rules">
              <el-form-item label="项目名称" prop="name">
                <el-input v-model.trim="projectForm.name"  placeholder="项目名称与git代码库名称一致" @blur="isExist"></el-input>
              </el-form-item >

              <el-form-item label="项目类型" prop="type">
                <el-select v-model.trim="projectForm.type" placeholder="项目类型" style="width: 100%">
                  <el-option label="VUE" value="VUE"></el-option>
                  <el-option label="JAVA" value="JAVA"></el-option>
                  <!--<el-option label="Python" value="Python"></el-option>-->
                  <el-option label="其他" value="其他"></el-option>
                </el-select>

              </el-form-item>
              <el-form-item label="git地址" prop="repository">
                <el-input v-model.trim="projectForm.repository" placeholder="git@git.huashenghaoche.com:project.git"></el-input>
              </el-form-item>
              <el-form-item label="服务端口" prop="server_port">
                <el-input v-model.trim="projectForm.server_port" placeholder="0" style="width: 30%"></el-input>
              </el-form-item>
              <el-form-item label="下载路径" prop="download_path">
                <el-input v-model.trim="projectForm.download_path" placeholder="http://www.nginx.org/download/"></el-input>
              </el-form-item>
              <el-form-item label="部署路径" prop="server_path">
                <el-input v-model.trim="projectForm.server_path" placeholder="/opt/data/"></el-input>
              </el-form-item>

              <el-form-item label="描述" prop="describe">
                <el-input v-model.trim="projectForm.describe" type="textarea" placeholder="Enter something..."></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitForm()">立即创建</el-button>
                <el-button @click="resetForm('projectForm')">重置</el-button>
              </el-form-item>
        </el-form>
          </el-tab-pane>
          <el-tab-pane label="OTHER"></el-tab-pane>
        </el-tabs>
      </el-card>
    </div>

  </hs-layout_auto>
</template>

<script>
  export default {
    data () {
      return {
        projectForm: {
          'name': '',
          'type': '',
          'repository': '',
          'server_port': '',
          'server_path': '',
          'project_admin': '',
          'download_path': '',
          'host_list': [],
          'describe': ''
        },
        rules: {
          name: [{required: true, message: '请输入项目名称', trigger: 'blur'}],
          type: [{required: true, message: '请选择记录类型', trigger: 'change'}],
          repository: [{required: true, message: '输入git地址', trigger: 'blur'}],
          download_path: [{required: true, message: '输入下载路径', trigger: 'blur'}]
          // host_list: [{required: true, message: '输入主机地址', trigger: 'blur'}],
          // describe: [{required: true, message: '输入描述', trigger: 'blur'}]
        }
      };
    },
    activated: function () {

    },
    methods: {
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      removeDomain(env, item) {
        if (env === 'pro_address') {
          var index = this.projectForm.pro_address.indexOf(item)
          if (index !== -1) {
            this.projectForm.pro_address.splice(index, 1)
          }
        } else {
          index = this.projectForm.dev_address.indexOf(item)
          if (index !== -1) {
            this.projectForm.dev_address.splice(index, 1)
          }
        }


      },
      addDomain() {
        this.projectForm.dev_address.push({
          value: '',
          key: Date.now()
        });
      },
      isExist () {
        console.log('name', this.projectForm);
        this.$http.get(this.deploy_api + 'list/', {params: this.projectForm['name']}).then((resp) => {
          if (resp.data.status) {
            return true;
          } else {
            this.projectForm['name'] = '';
            this.$alert(resp.data.msg);
          }
        }).catch((error) => {
          this.resForm = 'error'
          console.log(this.error)
        })
      },
      submitForm() {
        this.$http.post(this.deploy_api + 'add_item/', this.projectForm).then((resp) => {
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '信息已提交',
              type: 'success'
            });
            this.projectForm['name'] = '';
            this.projectForm['type'] = '';
            this.projectForm['repository'] = '';
            this.projectForm['server_port'] = '';
            this.projectForm['download_path'] = '';
            this.projectForm['describe'] = '';
            this.projectForm['server_path'] = '';
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
  .rightbutton {
    float: right;
    margin-bottom: 15px;
    /*border: 1px solid rgb(191, 217, 204);*/
    /*background-color: #149C4C;*/
    /*color: white;*/
  }
  /*.el-textarea__inner {*/
    /*width: 65%;*/
  /*}*/

  /*.el-select, .el-input {*/
    /*width: 65%;*/
  /*}*/

  .el-form {
    background-color: white;
    padding: 50px;
    width: 70rem;
    /*border: 1px solid rgb(191, 217, 204);*/
  }

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }
</style>
