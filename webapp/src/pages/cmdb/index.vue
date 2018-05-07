<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="tabs_class">
        <el-card class="box-card" style="width: 100%">
          <div slot="header" class="clearfix">
              <span style="color: #149C4C; font-weight: 700; font-size: 16px">
                主机信息
              </span>
            <span>
                <router-link class="right" :to="{name: '031-1'}">
                        <el-button class="rightbutton" type="primary" @click="">新建主机</el-button>
                </router-link>

              </span>
          </div>
          <div style="margin-top: 15px; margin-bottom: 35px; width: 30%; float: right;">
            <el-input placeholder="请输入查询条件" v-model.trim="searchForm.input5" class="input-with-select">
              <el-select v-model="searchForm.select" slot="prepend" placeholder="查询类别">
                <el-option label="管理员" value="1"></el-option>
                <el-option label="运行环境" value="2"></el-option>
                <el-option label="业务线" value="3"></el-option>
              </el-select>
              <el-button slot="append" icon="el-icon-search" @click="submitSearch">
                <img src="../../assets/search.png" width="100%" height="100%" style="width: 20px">
              </el-button>
            </el-input>
          </div>
              <el-table :data="resForm" style="width: 100%" height="650"  :default-sort = "{prop: 'id', order: 'descending'}">
                <el-table-column prop="id" label="ID" sortable>
                </el-table-column>
                <el-table-column prop="owner" label="管理员">
                </el-table-column>
                <el-table-column prop="address" label="主机地址">
                </el-table-column>
                <el-table-column prop="be_app" label="业务线">
                </el-table-column>
                <el-table-column prop="os" label="系统版本">
                </el-table-column>
                <el-table-column prop="hostname" label="主机名">
                </el-table-column>
                <el-table-column prop="host_env" label="运行环境">
                </el-table-column>
                <el-table-column prop="host_type" label="主机类型">
                </el-table-column>
                <el-table-column prop="pyh_host" label="宿主机">
                </el-table-column>
                <el-table-column prop="status" label="状态">
                </el-table-column>

                <el-table-column prop="created" label="创建时间" sortable>
                </el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button type="info" size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button @click="handleClick(scope.row)" type="danger" size="mini">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>

        </el-card>
      </div>
    </div>

    <el-dialog v-model="enable_mod" :visible.sync="modResource">
      <el-col slot="title" class="dialog_title">
        <span>{{rowForm.address}}</span>
      </el-col>
        <el-form :model="modResource" ref="modResource" label-width="140px">
          <el-form-item label="ID" prop="id">
            <el-input v-model.trim="rowForm.id" placeholder="请输入主机地址"></el-input>
          </el-form-item>
          <el-form-item label="IP地址" prop="address">
            <el-input v-model.trim="rowForm.address" placeholder="请输入主机地址"></el-input>
          </el-form-item>
          <el-form-item label="管理员" prop="owner">
            <el-input v-model.trim="rowForm.owner" placeholder="请输入主机管理员"></el-input>
          </el-form-item>
          <el-form-item label="业务线" prop="be_app">
            <el-input v-model.trim="rowForm.be_app" placeholder="请输入主机隶属的业务线"></el-input>
          </el-form-item>
          <el-form-item label="主机名" prop="hostname">
            <el-input v-model.trim="rowForm.hostname" placeholder="请输入主机名"></el-input>
          </el-form-item>
          <el-form-item label="系统版本" prop="os">
            <el-input v-model.trim="rowForm.os" placeholder="请输入操作系统版本"></el-input>
          </el-form-item>
          <el-form-item label="运行环境" prop="host_env">
            <el-select v-model.trim="rowForm.host_env" placeholder="请选择项目类型" style="width: 100%">
              <el-option label="pro" value="线上"></el-option>
              <el-option label="pre" value="测试"></el-option>
              <el-option label="dev" value="开发"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="主机类型" prop="host_type">
            <el-input v-model.trim="rowForm.host_type" placeholder="请输入主机类型,虚拟机or物理机or云主机"></el-input>
          </el-form-item>
          <el-form-item label="宿主机" prop="pyh_host">
            <el-input v-model.trim="rowForm.pyh_host" placeholder="请输入宿主机，如果有"></el-input>
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-input v-model.trim="rowForm.status"placeholder="请选择主机状态"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitMod('rowForm')">立即修改</el-button>
            <el-button @click="resetForm('rowForm')">重置</el-button>
          </el-form-item>
        </el-form>
    </el-dialog>

    <el-dialog v-model="enable_search" :visible.sync="modResource">
      <el-table :data="searchRes" :default-sort = "{prop: 'id', order: 'descending'}">
        <el-table-column prop="id" label="ID" sortable>
        </el-table-column>
        <el-table-column prop="owner" label="管理员">
        </el-table-column>
        <el-table-column prop="address" label="主机地址">
        </el-table-column>
        <el-table-column prop="be_app" label="业务线">
        </el-table-column>
        <el-table-column prop="os" label="系统版本">
        </el-table-column>
        <el-table-column prop="hostname" label="主机名">
        </el-table-column>
        <el-table-column prop="host_env" label="运行环境">
        </el-table-column>
        <el-table-column prop="host_type" label="主机类型">
        </el-table-column>
        <el-table-column prop="pyh_host" label="宿主机">
        </el-table-column>
        <el-table-column prop="status" label="状态">
        </el-table-column>
        <el-table-column prop="created" label="创建时间" sortable>
        </el-table-column>
      </el-table>
    </el-dialog>
  </hs-layout_auto>
</template>

<script>
  export default {
    data () {
      return {
        searchForm: {
          'input5': '',
          'select': '',
          'owner': '',
          'host_env': '',
          'be_app': ''
        },
        enable_mod: false,
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
        delResource: {
          'id': ''
        },
        modResource: {},
        resForm: '',
        rowForm: '',
        enable_add: false,
        enable_search: false,
        searchRes: ''
      };
    },
    activated: function () {
      this.get_all_list();
    },
    methods: {
      get_all_list() {
        console.log(this.deploy_api + 'list/')
        this.$http.get(this.cmdb_api + 'list/').then((resp) => {
          // console.log('this resp', resp.data)
          this.resForm = resp.data.data;
          // console.log('resform', this.resForm)
        }).catch((error) => {
          this.resForm = 'error'
          console.log(this.resForm)
        })
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      handleEdit(index, row) {
        console.log('handleEdit', index, row);
        this.rowForm = row;
        this.enable_mod = !this.enable_mod;
      },
      submitMod() {
        console.log('submitmod', this.modResource, this.rowForm)
        this.$http.post(this.cmdb_api + 'mod_item/', this.rowForm).then((resp) => {
          console.log('resp', resp)
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '删除成功',
              type: 'success'
            });
            window.location = '/cmdb/index';
          } else {
            this.$notify.error({
              title: '错误',
              message: '删除失败'
            });
            // alert(resp.data.status + resp.data.message)
            console.log(resp.data.status + resp.data.message);

          }
        }).catch((error) => {

        })
      },
      handleClick(row) {
        console.log('handleClick', row);
        this.modResource = row;
        this.$http.post(this.cmdb_api + 'del_item/', this.modResource).then((resp) => {
          console.log('resp', resp)
          if (resp.data.status) {
            this.$notify({
              title: '成功',
              message: '编辑成功',
              type: 'success'
            });
            window.location = '/cmdb/index';
          } else {
            this.$notify.error({
              title: '错误',
              message: '编辑失败'
            });
            // alert(resp.data.status + resp.data.message)
            console.log(resp.data.status + resp.data.message);

          }
        }).catch((error) => {

        })
      },
      checkInput() {
        if (this.searchForm.input5.length === 0) {
          this.$alert('请输入查询条件!');
          return false
        }
        return true
      },
      submitSearch() {
        // console.log('submitSearch', this.searchForm);
        if (this.searchForm.select === '1') {
          this.searchForm.owner = this.searchForm.input5;
          this.searchForm['host_env'] = '';
          this.searchForm['be_app'] = '';
          console.log(this.searchForm)
        } else if (this.searchForm.select === '2') {
          this.searchForm.host_env = this.searchForm.input5;
          this.searchForm['owner'] = '';
          this.searchForm['be_app'] = '';
        } else if (this.searchForm.select === '3') {
          this.searchForm.be_app = this.searchForm.input5;
          this.searchForm['host_env'] = '';
          this.searchForm['owner'] = '';
        } else {
          this.$alert('请选择查询类别！')
          return false
        }
        if (this.checkInput()) {
          // console.log('check', this.searchForm.input5)
          this.$http.post(this.cmdb_api + 'search_one/', this.searchForm).then((resp) => {
            // console.log('this.searchForm', resp.data.data);
            this.searchRes = resp.data.data;
            if (resp.data.status) {
              this.enable_search = !this.enable_search;
              this.searchForm.select = '';
              this.searchForm.input5 = '';
              // console.log(this.searchRes)
            } else {
              this.$alert(this.searchRes)
            }
          }).catch((error) => {
            console.log(error)
          })
        }
      }
    }
  }
</script>
<style>
  .el-select .el-input {
    width: 130px;
  }
  .input-with-select .el-input-group__prepend {
    background-color: #fff;
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
    width: 80%;
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
</style>
