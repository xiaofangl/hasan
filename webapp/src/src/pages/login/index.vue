<template>
  <div style="height: 100%; width: 100%; ">
    <div class="bclass">
      <el-card style="width: 30%; margin-left: 35%">
        <el-tabs v-model="activeName2">
          <el-tab-pane label="登录" name="first">
            <el-form :model="loginForm" ref="loginForm" class="fclass" :rules="loginForms">
              <el-form-item prop="username" label="用  户">
                <el-input v-model.trim="loginForm.username" placeholder="请输入用户名"></el-input>
              </el-form-item>
              <el-form-item prop="password" label="密  码">
                <el-input v-model.trim="loginForm.password" placeholder="请输入密码" type="password"
                          @keyup.enter.native="submitLogin"></el-input>
              </el-form-item>
              <el-form-item style="margin-left: 100px; width: 45%">
                <el-button type="primary" @click="submitLogin" style="padding-left: 35px; padding-right: 35px;">登 录
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="注册" name="second">
            <el-form :model="registerForm" ref="registerForm" class="fclass" :rules="registerForms">
              <el-form-item prop="username" label="用  户">
                <!--<span>-->
                <!--<img class="imgClass" src="../../assets/user.png"/>-->
                <!--</span>-->
                <el-input v-model.trim="registerForm.username" placeholder="由英文字母组成，尽量使用邮箱前缀"></el-input>
              </el-form-item>
              <el-form-item prop="password" label="密  码">
                <el-input v-model.trim="registerForm.password" placeholder="请输入8位密码" type="password"></el-input>
              </el-form-item>
              <el-form-item prop="email" label="邮箱">
                <el-input v-model.trim="registerForm.email" placeholder="请输入邮箱" @keyup.enter.native="submitRegist">
                  <template slot="append">@huashenghaoche.com</template>
                </el-input>
              </el-form-item>
              <el-form-item style="margin-left: 100px; width: 45%">
                <el-button type="primary" @click="submitRegist" style="padding-left: 35px; padding-right: 35px;">注 册
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="忘记密码" name="third">
            <el-form :model="resetPawd" ref="resetPawd" class="fclass" :rules="resetPawds">
              <el-form-item prop="username" label="用户名">
                <el-input v-model.trim="resetPawd.username" placeholder="请输入用户名"></el-input>
              </el-form-item>
              <el-form-item prop="mail" label="邮箱">
                <el-input v-model.trim="resetPawd.mail" placeholder="请输入邮箱">
                  <template slot="append">@huashenghaoche.com</template>
                </el-input>
              </el-form-item>
              <!--<el-form-item prop="secondPwd" label="再一次" >-->
              <!--<el-input v-model.trim="resetPawd.secondPwd" placeholder="请再输入一次" type="password" @keyup.enter.native="submitReset"></el-input>-->
              <!--</el-form-item>-->
              <el-form-item style="margin-left: 100px; width: 45%">
                <el-button type="primary" @click="submitReset" style="padding-left: 35px; padding-right: 35px;">发送邮件
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
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
        formLabelWidth: '108px',
        name: '',
        loginForm: {
          'username': '',
          'password': ''
        },
        registerForm: {
          'username': '',
          'password': '',
          'email': ''
        },
        resetPawd: {
          'title': 'To reset your password',
          'username': '',
          'mail': ''
        },
        // 要做密码复杂性校验。。
        loginForms: {
          username: [{required: true, message: '用户名称不能为空', trigger: 'blur'}],
          password: [{required: true, message: '密码称不能为空', trigger: 'blur'}]
        },
        registerForms: {
          username: [{required: true, message: '用户名称不能为空', trigger: 'blur'}],
          password: [{required: true, message: '密码称不能为空', trigger: 'blur'}],
          email: [{required: true, message: 'email称不能为空', trigger: 'blur'}]
        },
        resetPawds: {
          username: [{required: true, message: '用户名称不能为空', trigger: 'blur'}],
          mail: [{required: true, message: '邮箱不正确', trigger: 'blur'}],
          secondPwd: [{required: true, message: '密码不一致', trigger: 'blur'}]
        }
      }
    },
    created: function () {
      if (this.$route.params.hasOwnProperty('h')) {
        this.h = this.$route.params.h
      }
    },
    methods: {
      checkInput() {
        // let numbers = /^1\d{10}$/;
        if (this.loginForm.password.length === 0) {
          this.$alert('请输入密码!');
          return false
        }
        return true
      },
      checkRegist() {
        if (this.registerForm.username.length === 0) {
          this.$alert('请输入用户名!');
          return false
        } else if (this.registerForm.password.length < 8) {
          this.$alert('密码不能少于8位!');
          return false
        } else if (this.registerForm.email.length === 0) {
          this.$alert('请输入邮箱地址!');
          return false
        }
        return true
      },
      checkReset() {
        console.log('check', this.resetPawd)
        if (this.resetPawd.username.length === 0) {
          this.$alert('请输入用户名!');
          return false
        } else if (this.resetPawd.firstPwd === 0) {
          this.$alert('请输入邮箱!');
          return false
        }
        return true
      },
      submitLogin() {
        if (this.checkInput()) {
          console.log('submitLogin', this.loginForm)
          this.$http.post(this.passport + 'login/', this.loginForm).then((resp) => {
            console.log('submitLogin', resp);
            if (!resp.data.status) {
              this.$alert(resp.data.msg);
            } else {
              window.localStorage.setItem('userhashid', resp.data.userhashid);
              window.localStorage.setItem('username', resp.data.username);
              window.localStorage.setItem('is_admin', resp.data.is_admin);
              window.localStorage.setItem('user_group', resp.data.user_group);
              this.$http.defaults.headers.common['Authorization'] = resp.data.userhashid;
              if (this.h) {
                this.$router.go(-1)
              } else {
                window.location = '/myself';
              }
            }
          }).catch((error) => {
            console.log(error)
          })
        }
      },
      submitRegist() {
        // console.log('submitRegist', this.registerForm)
        if (this.checkRegist()) {
          this.$http.post(this.passport + 'signup/', this.registerForm).then((resp) => {
            console.log('submitRegist', resp);
            if (!resp.data.status) {
              this.warnMessage(resp.data.msg);
            } else {
              if (resp.data.code === '0') {
                console.log('submitRegist', resp);
                window.localStorage.setItem('userhashid', resp.data.userhashid);
                window.localStorage.setItem('username', resp.data.username);
                window.localStorage.setItem('is_admin', resp.data.is_admin);
                window.localStorage.setItem('user_group', resp.data.user_group);
                this.$http.defaults.headers.common['Authorization'] = resp.data.userhashid;
                this.user_id = resp.data.user_id;
                if (this.h) {
                  this.$router.go(-1)
                } else {
                  console.log('submitRegist', resp);
                  window.location = '/myself';
                }
              } else if (resp.data.code === '1') {
                console.log(resp.data.message);
                this.activeName2 = 'first';
                this.$alert(resp.data.msg);
              }
            }
          }).catch((error) => {
            console.log(error)
          })
        }
      },
      submitReset() {
        if (this.checkReset()) {
          console.log('this.resetPawd', this.resetPawd)
          this.$http.post(this.passport + 'reset_pawd_api/', this.resetPawd).then((resp) => {
            console.log('submitReset', resp);
            if (!resp.data.status) {
              // this.$alert(resp.data.msg);
              console.log(resp.data.msg);
              window.location = '/';
              // window.close();
            } else {
              if (resp.data.code === '0') {
                window.localStorage.setItem('userhashid', resp.data.userhashid);
                window.localStorage.setItem('username', resp.data.username);
                window.localStorage.setItem('is_admin', resp.data.is_admin);
                window.localStorage.setItem('user_group', resp.data.user_group);
                this.$http.defaults.headers.common['Authorization'] = resp.data.userhashid;
                this.user_id = resp.data.user_id;
                if (this.h) {
                  this.$router.go(-1)
                } else {
                  window.location = '/';
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
