<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class"></div>

      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
              <span style="color: #149C4C; font-weight: 700; font-size: 16px">
                增加资源(单台添加)
              </span>
          <span>
                <router-link class="right" :to="{name: '031'}">
                        <el-button class="rightbutton" type="primary" @click="">资源列表</el-button>
                </router-link>

              </span>
        </div>
            <el-form :model="resourceForm" ref="resourceForm" label-width="140px" :rules="resourceForms">
              <el-form-item label="IP地址" prop="address">
                <el-input v-model.trim="resourceForm.address" placeholder="请输入主机地址"></el-input>
              </el-form-item>
              <el-form-item label="管理员" prop="owner">
                <el-input v-model.trim="resourceForm.owner" placeholder="请输入主机管理员"></el-input>
              </el-form-item>
              <el-form-item label="业务线" prop="be_app">
                <el-input v-model.trim="resourceForm.be_app" placeholder="请输入主机隶属的业务线"></el-input>
              </el-form-item>
              <el-form-item label="主机名" prop="hostname">
                <el-input v-model.trim="resourceForm.hostname" placeholder="请输入主机名"></el-input>
              </el-form-item>
              <el-form-item label="系统版本" prop="os">
                <el-input v-model.trim="resourceForm.os" placeholder="请输入操作系统版本"></el-input>
              </el-form-item>
              <el-form-item label="运行环境" prop="host_env">
                <el-select v-model.trim="resourceForm.host_env" placeholder="请选择项目类型" style="width: 100%">
                  <el-option label="pro" value="线上"></el-option>
                  <el-option label="pre" value="测试"></el-option>
                  <el-option label="dev" value="开发"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="主机类型" prop="host_type">
                <el-input v-model.trim="resourceForm.host_type" placeholder="请输入主机类型,虚拟机or物理机or云主机"></el-input>
              </el-form-item>
              <el-form-item label="宿主机" prop="pyh_host">
                <el-input v-model.trim="resourceForm.pyh_host" placeholder="请输入宿主机，如果有"></el-input>
              </el-form-item>
              <el-form-item label="状态" prop="status">
                <el-input v-model.trim="resourceForm.status"placeholder="请选择主机状态"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitAdd">立即创建</el-button>
                <el-button @click="resetForm('resourceForm')">重置</el-button>
              </el-form-item>
            </el-form>

      </el-card>
    </div>

  </hs-layout_auto>
</template>

<script>
  export default {
    data () {
      return {
        resourceForm: {
          'address': '',
          'owner': '',
          'be_app': '',
          'os': '',
          'hostname': '',
          'host_type': '',
          'pyh_host': '',
          'host_env': '',
          'is_del': '',
          'status': '',
          'created': ''

        },
        resourceForms: {
          address: [{required: true, message: '请输入', trigger: 'blur'}],
          owner: [{required: true, message: '请输入', trigger: 'blur'}],
          be_app: [{required: true, message: '请输入', trigger: 'blur'}],
          os: [{required: true, message: '请输入', trigger: 'blur'}],
          hostname: [{required: true, message: '请输入', trigger: 'blur'}],
          host_type: [{required: true, message: '请输入', trigger: 'blur'}],
          pyh_host: [{required: true, message: '请选择', trigger: 'change'}],
          host_env: [{required: true, message: '请输入', trigger: 'blur'}],
          status: [{required: true, message: '请输入', trigger: 'blur'}]
        }
      }
    },
    created: function () {
      if (this.$route.params.hasOwnProperty('h')) {
        this.h = this.$route.params.h
      }
    },
    methods: {
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      submitAdd() {
        console.log('resourceForm', this.resourceForm);
        this.$http.post(this.cmdb_api + 'add_item/', this.resourceForm).then((resp) => {
          console.log('resp', resp)
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success'
            });
            // window.location = '/cmdb/add_item';
            if (this.h) {
              this.$router.go(-1)
            } else {
              window.location = '/cmdb/add_item';
            }
          } else {
            this.$notify.error({
              title: '错误',
              message: '创建失败'
            });
            // alert(resp.data.status + resp.data.message)
            console.log(resp.data.status + resp.data.message);

          }

        }).catch((error) => {
          console.log(error)
          console.log('resp', error)

        })
      }
    }
  }
</script>
<style>
  .rightbutton {
    float: right;
    /*border: 1px solid rgb(191, 217, 204);*/
    /*background-color: #149C4C;*/
    /*color: white;*/
  }
  .el-textarea__inner {
    width: 65%;
  }

  .el-select, .el-input {
    width: 65%;
  }

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
