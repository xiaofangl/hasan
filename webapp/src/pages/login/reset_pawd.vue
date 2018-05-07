<template>
  <div style="height: 100%; width: 100%; ">
    <div class="bclass">
      <el-card style="width: 30%; margin-left: 35%">
        <div style="margin-top: 15px; margin-bottom: 15px; color: #149C4C;font-weight: 700; font-size: 16px ">重置密码</div>
        <el-tabs v-model="activeName2">
          <!--<el-tab-pane label="忘记密码" name="third">-->
          <el-form :model="resetPawd" ref="resetPawd" class="fclass" :rules="resetPawds">
            <el-form-item prop="username" label="用户名">
              <el-input v-model.trim="resetPawd.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item prop="firstPwd" label="新密码">
              <el-input v-model.trim="resetPawd.firstPwd" placeholder="请输入新密码" type="password"></el-input>
            </el-form-item>
            <el-form-item prop="secondPwd" label="再一次">
              <el-input v-model.trim="resetPawd.secondPwd" placeholder="请再输入一次" type="password"
                        @keyup.enter.native="submitReset"></el-input>
            </el-form-item>
            <el-form-item style="margin-left: 100px; width: 45%">
              <el-button type="primary" @click="submitReset" style="padding-left: 35px; padding-right: 35px;">更改密码
              </el-button>
            </el-form-item>
          </el-form>
          <!--</el-tab-pane>-->
        </el-tabs>
      </el-card>
    </div>
  </div>


</template>

<script>
  export default {
    data() {
      return {
        activeName2: 'first',
        resetPawd: {
          'username': '',
          'firstPwd': '',
          'secondPwd': ''
        },
        resetPawds: {
          username: [{required: true, message: '用户名称不能为空', trigger: 'blur'}],
          firstPwd: [{required: true, message: '新密码格式不正确', trigger: 'blur'}],
          secondPwd: [{required: true, message: '密码不一致', trigger: 'blur'}]
        }
      }
    },
    methods: {
      checkReset() {
        console.log('check', this.resetPawd)
        if (this.resetPawd.username.length === 0) {
          this.$alert('请输入用户名!');
          return false
        } else if (this.resetPawd.firstPwd !== this.resetPawd.secondPwd) {
          this.$alert('密码输入不一致，请重新输入!');
          return false
        }
        return true
      },
      submitReset() {
        if (this.checkReset()) {
          this.$http.post(this.passport + 'reset_password/', this.resetPawd).then((resp) => {
            console.log('submitReset', resp);
            if (!resp.data.status) {
              this.$alert(resp.data.msg);
            } else {
              if (resp.data.code === '0') {
                window.localStorage.setItem('userhashid', resp.data.userhashid);
                window.localStorage.setItem('username', resp.data.username);
                window.localStorage.setItem('is_admin', resp.data.is_admin);
                this.$http.defaults.headers.common['Authorization'] = resp.data.userhashid;
                this.user_id = resp.data.user_id;
                if (this.h) {
                  this.$router.go(-1)
                } else {
                  window.location = '/myself';
                }
              } else if (resp.data.code === '1') {
                this.activeName2 = 'first';
                this.$refs[this.resetPawd].resetFields();
                this.$alert(resp.data.msg);

              }
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
  .bclass {
    margin-top: 150px;
    padding-top: 130px;
    text-align: center;
    width: 100%;
    height: 600px;
    font-size: 14px;
    background: url('../../assets/feb_last_banner_2018.jpg') center center no-repeat;
  }

  .fclass {
    padding-top: 20px;
    width: 89%;
  }

  .el-select, .el-input {
    width: 76%;
  }

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }

  .el-tabs__item {
    /*padding: 0 4.13rem;*/
    padding: 0 36px;
  }

  .imgClass {
    width: 0.8rem;
    height: 0.75rem;

  }
</style>
