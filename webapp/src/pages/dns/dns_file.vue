<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">

      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
            <span style="color: #149C4C; font-weight: 700; font-size: 16px">
              当前文件
            </span>
        </div>
        <el-collapse v-for="item in res_data">
          <el-row>
            <el-col :span="10">
              <div style="padding-top: 15px; padding-left: 15px;">
                <span style="color: #149C4C; font-weight: 700; font-size: 16px">{{item[0]}}</span>
              </div>

            </el-col>
            <el-col :span="14">
              <div class="grid-content bg-purple-light">
                <!--<el-collapse-item title="OPEN">-->
                <el-table :data="item[1]" style="width: 100%">
                  <el-table-column prop="ip" label="运行主机" sytle="width: 50%">
                  </el-table-column>
                  <el-table-column prop="env" label="主机环境" sytle="width: 50%">
                  </el-table-column>
                </el-table>
                <!--</el-collapse-item>-->
              </div>
            </el-col>

          </el-row>

        </el-collapse>
      </el-card>

      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
            <span style="color: #149C4C; font-weight: 700; font-size: 16px">
              上传文件
            </span>
        </div>
        <div>
          <el-form :model="uploadForm" ref="uploadForm" label-width="140px" :rules="uploadForms">
            <el-form-item label="文件名称" prop="name">
              <el-upload class="upload-demo" :action="filePath" :http-request="myUpload" :on-change="handleChange"
                         :before-remove="beforeRemove">
                <el-button size="small" type="primary">点击上传</el-button>
                <!--<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
              </el-upload>
            </el-form-item>
            <el-form-item label="同步主机" prop="type">
              <el-checkbox-group v-model="uploadForm.host">
                <el-checkbox label="lan_dns主机组" name="host"></el-checkbox>
                <el-checkbox label="wan_dns主机组" name="host"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitUload('updateForm')">立即同步</el-button>
              <el-button @click="resetRecode('updateForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
            <span style="color: #149C4C; font-weight: 700; font-size: 16px">
              新建文件
            </span>
        </div>
        <div>
          <el-form :model="ruleForm" ref="ruleForm" label-width="140px" :rules="ruleForms">
            <el-form-item label="文件名称" prop="name">
              <el-input v-model.trim="ruleForm.name" placeholder="请输入zone文件名称如：xxx.mmm.zone"
                        @blur=isExist(ruleForm.name)></el-input>
            </el-form-item>
            <el-form-item label="同步主机" prop="type">
              <el-checkbox-group v-model="ruleForm.host">
                <el-checkbox label="lan_dns主机组" name="host"></el-checkbox>
                <el-checkbox label="wan_dns主机组" name="host"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
              <el-button @click="resetRecode('ruleForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
            <span style="color: #149C4C; font-weight: 700; font-size: 16px">
              删除文件
            </span>
        </div>
        <div>
          <el-form :model="delForm" ref="delForm" label-width="140px" :rules="delForms">
            <el-form-item label="文件名称" prop="name">
              <el-select v-model="delForm.name" placeholder="请选择项文件" @change="hanldFile(delForm.name)">
                <el-option :lable="i[0]" :value="i[0]" v-for="i in res_data"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="同步主机" prop="type">
              <el-checkbox-group v-model="delForm.host">
                <el-checkbox label="lan_dns主机组" name="host" v-if="isLan === 0"></el-checkbox>
                <el-checkbox label="wan_dns主机组" name="host" v-if="isWan === 0"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitDel('delForm')">立即删除</el-button>
              <el-button @click="resetRecode('delForm')">重置</el-button>
            </el-form-item>
          </el-form>

        </div>
      </el-card>


      <el-card class="box-card" style="width: 100%">
        <div slot="header" class="clearfix">
            <span style="color: #149C4C; font-weight: 700; font-size: 16px">
              同步文件
            </span>
        </div>
        <div>
          <el-form :model="syncForm" ref="syncForm" label-width="90px" :rules="syncForms">
            <el-row>
              <el-col :span="12">
                <el-form-item label="文件名称" prop="name">
                  <el-select v-model="syncForm.name" placeholder="请选择同步文件">
                    <el-option :lable="i[0]" :value="i[0]" v-for="i in res_data"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="同步到 =>>" prop="type">
                  <el-checkbox-group v-model="syncForm.host">
                    <el-checkbox label="lan_dns主机组" name="host"></el-checkbox>
                    <el-checkbox label="wan_dns主机组" name="host"></el-checkbox>
                  </el-checkbox-group>
                </el-form-item>
              </el-col>
            </el-row>


            <el-form-item>
              <el-button type="primary" @click="submitSync('syncForm')">立即同步</el-button>
              <el-button @click="resetRecode('syncForm')">重置</el-button>
            </el-form-item>
          </el-form>

        </div>
      </el-card>

    </div>

    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%">
      <span>{{files}}</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
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
        fileList: [],
        filePath: this.upload_api,
        outerVisible: false,
        permissionMsg: '',
        activeNames: ['1'],
        dialogVisible: false,
        files: '',
        formLabelWidth: '108px',
        editableTabsValue: '2',
        ruleForm: {
          'name': '',
          'host': []
        },
        uploadForm: {
          'name': '',
          'host': []
        },
        delForm: {
          'id': '',
          'name': '',
          'host': []
        },
        syncForm: {
          'name': '',
          'host': [],
          'isExist': ''
        },
        res_data: '',
        isLan: 1,
        isWan: 1,
        one_row: {
          'file_name': '',
          'type': '',
          'host': '',
//          'ns_path': '-',
          'value': ''
//          'ttl': ''
        },
        test_vue: {
          'huashenghaoche.com.zone': ['huashenghaoche.com.zone', [{
            'ip': '172.30.5.135',
            'env': 'wan_dns主机组'
          }, {
            'ip': '172.30.5.145',
            'env': 'wan_dns主机组'
          }, {
            'ip': '192.168.99.252',
            'env': 'lan_dns主机组'
          }, {
            'ip': '192.168.99.251',
            'env': 'lan_dns主机组'
          }], 1]
        },
        ruleForms: {
          name: [{required: true, message: '文件名称不能为空', trigger: 'blur'}],
          host: [{type: 'array', required: true, message: '请至少选择一个主机组', trigger: 'change'}]
        },
        delForms: {
          name: [{required: true, message: '文件名称不能为空', trigger: 'blur'}],
          host: [{type: 'array', required: true, message: '请至少选择一个主机组', trigger: 'change'}]
        },
        syncForms: {
          name: [{required: true, message: '文件名称不能为空', trigger: 'blur'}],
          host: [{type: 'array', required: true, message: '请至少选择一个主机组', trigger: 'change'}]
        },
        uploadForms: {
          name: [{required: true, message: '文件名称不能为空', trigger: 'blur'}],
          host: [{type: 'array', required: true, message: '请至少选择一个主机组', trigger: 'change'}]
        }
      }
    },
    activated: function () {
      this.get_all_list();
    },
    methods: {
      get_all_list() {
        console.log('this is get_all_list')
        this.$http.get(this.dns_api + 'file_list').then((resp) => {
          this.res_data = resp.data.data;
          // this.res_data = this.test_vue;
          // console.log('resp', resp)
          // this.permissionControl(resp);
        }).catch((error) => {
          this.res_data = 'error';
          // console.log(error);
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
      isExist(files) {
        // console.log('isexist', files);
        let c;
        for (c in this.res_data) {
          if (files === c) {
            this.ruleForm.name = '';
            this.files = files + ' is exist..';
            this.dialogVisible = true;
            // this.$alert(this.files, '提示', {
            //   confirmButtonText: '确定'
            // });
          }
        }
      },
      hanldFile(fiels) {
        console.log('hanldFile', fiels);
        this.isLan = 1;
        this.isWan = 1;
        let i;
        let host_info;
        for (i in this.res_data) {
//                console.log('res_data', this.res_data[i][1])
//                console.log('i',i)
          if (i === fiels) {
            this.delForm.id = this.res_data[i][2]
//                    console.log(i, this.delForm.name)
            for (host_info in this.res_data[i][1]) {
//                        console.log('host_info', this.res_data[i][1], this.res_data[i][1][host_info], this.res_data[i][1][host_info]['env'])
              if (this.res_data[i][1][host_info]['env'] === 'lan_dns主机组') {

                this.isLan = 0;
              } else if (this.res_data[i][1][host_info]['env'] === 'wan_dns主机组') {
                this.isWan = 0;
              }
            }
          }
        }
      },
      myUpload(content) {
        // console.log('myUpload', content.file, this.uploadForm);
        // this.uploadForm.content = content.file;
        this.uploadForm.name = content.file.name;
        this.$http.post(this.upload_api, content.file).then((resp) => {
          content.onSuccess('配时文件上传成功')
        }).catch((error) => {
          console.log(error)
        })
      },
      beforeRemove(file, fileList) {
        console.log('beforeRemove')
        return this.$confirm(`确定移除`);
      },
      handlePreview(file) {
        console.log('handlePreview');
        console.log(file, this.fileList)
      },
      handleChange(file, fileList) {
        console.log('handleChange');
        console.log(file, this.fileList);
        // this.$http.post(this.upload_api, file).then((resp) => {
        //   console.log('resp', resp)
        // }).catch((error) => {
        //   console.log(error)
        // })
      },
      handleRemove(file) {
        console.log('handleRemove');
        console.log(file, this.fileList)
      },
      submitUload() {
        console.log('submitUload', this.uploadForm)
        this.$http.post(this.dns_api + 'upload_file/', this.uploadForm).then((resp) => {
          this.permissionControl(resp);
          console.log('resp', resp)
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success'
            });
            this.get_all_list();
            this.uploadForm.host = [];
            this.uploadForm.name = ''
          } else {
            // alert(resp.data.status + resp.data.message);
            console.log(resp.data.status + resp.data.message)
          }
        }).catch((error) => {
          console.log(error);
          this.$notify.error({
            title: '错误',
            message: '创建失败'
          });
        })
      },
      submitForm(forms) {
//            this.ruleForm.host = this.ruleForm.host.toString();
        console.log('forms', this.ruleForm);
        this.$refs[forms].validate((vaild) => {
          if (vaild) {
            this.$http.post(this.dns_api + 'add_file/', this.ruleForm).then((resp) => {
              this.permissionControl(resp);
              console.log('resp', resp)
              if (resp.data.status) {
                this.$notify({
                  title: '成功',
                  message: '创建成功',
                  type: 'success'
                });
                this.get_all_list();
                this.ruleForm.host = [];
                this.ruleForm.name = ''
              } else {
                // alert(resp.data.status + resp.data.message);
                console.log(resp.data.status + resp.data.message)
              }
            }).catch((error) => {
              console.log('resp', error)
              this.$notify.error({
                title: '错误',
                message: '创建失败'
              });
            })
          } else {
            return false;
          }
        })
      },
      submitDel(forms) {
        console.log('delforms', this.delForm);
        this.$refs[forms].validate((vaild) => {
          if (vaild) {
            this.$http.post(this.dns_api + 'del_file/', this.delForm).then((resp) => {
              this.permissionControl(resp);
              console.log('resp', resp)
              if (resp.data.status) {
                this.$notify({
                  title: '删除',
                  message: '删除成功',
                  type: 'success'
                });
                this.get_all_list();
                this.delForm.host = [];
                this.delForm.name = '';
                this.delForm.id = '';
                this.isLan = 1;
                this.isWan = 1;
              } else {
                // alert(resp.data.status + resp.data.message)
                console.log(resp.data.status + resp.data.message);
              }
            }).catch((error) => {
              this.$notify({
                title: '删除',
                message: '删除失败',
                type: 'success'
              });
              console.log(error)
            })
          } else {
            return false;
          }
        })
      },
      submitSync(forms) {
        console.log('forms', this.syncForm);

        this.$refs[forms].validate((vaild) => {
          if (vaild) {
            this.$http.post(this.dns_api + 'copy_file/', this.syncForm).then((resp) => {
              this.permissionControl(resp);
              console.log('resp', resp)
              if (resp.data.status) {
                this.$notify({
                  title: '成功',
                  message: '同步成功',
                  type: 'success'
                });
                this.get_all_list();
                this.syncForm.host = [];
                this.syncForm.name = ''
//                            this.syncForm.isExist=''
              } else {
                // alert(resp.data.status + resp.data.message)
                console.log(resp.data.status + resp.data.message);
              }
            }).catch((error) => {
              console.log('resp', error)
              this.$notify.error({
                title: '错误',
                message: '同步失败'
              });
            })
          } else {
            return false;
          }
        })
      },
      resetRecode(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style>
  input[type="file"] {
    display: none;
  }

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
