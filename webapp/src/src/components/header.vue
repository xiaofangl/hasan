<template>
  <header id="header">

    <!--<div id="logo-group">-->
    <!--<span id="logo"><img src="../assets/logo.png" alt="youmuto"> </span>-->
    <!--</div>-->

    <div class="hidden-xs" style="color: #FFF; margin-left: 10px">
      <h1>hasan-哈桑</h1>
    </div>

    <div class="pull-right">
      <el-dropdown style="color: white; line-height: 50px; font-size: 120%; cursor: pointer" trigger="click" @command="handleCommand">
                <span class="el-dropdown-link">
                    {{username}}
                    <i class="el-icon-caret-bottom el-icon--right" style="font-size: 50%"></i>
                </span>
        <el-dropdown-menu slot="dropdown" style="width: 180px">
          <el-dropdown-item command="permission_manage" v-if="isAdmin == 1">权限管理</el-dropdown-item>
          <el-dropdown-item command="myself" >个人中心</el-dropdown-item>
          <!--<el-dropdown-item>退出</el-dropdown-item>-->
          <el-dropdown-item divided command="logout">退出</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </header>
</template>

<script>
  export default {
    data() {
      return {
        username: '',
        isAdmin: 0
      }
    },
    mounted() {
      this.checkUser();
      this.bus.$on('search', function (val) {
        this.search = val
      }.bind(this));
      this.username = window.localStorage.getItem('username');
      // this.isAdmin = window.localStorage.getItem('is_admin');
      if (window.localStorage.getItem('is_admin') === 'true') {
        this.isAdmin = 1;
      }
    },
    methods: {
      checkUser() {
        let has_permissions = Boolean(window.localStorage.getItem('user_group'));
        if (has_permissions) {
          has_permissions = window.localStorage.getItem('user_group').split(',');
          if (has_permissions.length > 1) {
            console.log(has_permissions);
            for (let i in has_permissions) {
              if (has_permissions[i] === 'deploy_admin') {
                this.isdeploy_admin = true;
                this.bus.$emit('isdeploy_admin', true)
                console.log('checkuser', this.isdeploy_admin)
              } else if (has_permissions[i] === 'dns_api_admin') {
                this.isdns_admin = true;
                this.bus.$emit('isdns_admin', true)
                console.log('checkuser', this.isdns_admin)
              } else if (has_permissions[i] === 'password_admin') {
                this.ispassword_admin = true;
                this.bus.$emit('ispassword_admin', true)
                console.log('checkuser', this.ispassword_admin)
              } else if (has_permissions[i] === 'app01_admin') {
                this.isapp01_admin = true;
                this.bus.$emit('isapp01_admin', true)
                console.log('checkuser', this.isapp01_admin)
              } else if (has_permissions[i] === 'cmdb_admin') {
                this.iscmdb_admin = true;
                this.bus.$emit('iscmdb_admin', true)
                console.log('checkuser', this.iscmdb_admin)
              }
            }
          } else if (has_permissions.length === 1) {
            if (has_permissions === 'deploy_admin') {
              this.isdeploy_admin = true;
              this.bus.$emit('isdeploy_admin', true)
              console.log('checkuser', this.isdeploy_admin)
            } else if (has_permissions === 'dns_api_admin') {
              this.isdns_admin = true;
              this.bus.$emit('isdns_admin', true)
              console.log('checkuser', this.isdns_admin)
            } else if (has_permissions === 'password_admin') {
              this.ispassword_admin = true;
              this.bus.$emit('ispassword_admin', true)
              console.log('checkuser', this.ispassword_admin)
            } else if (has_permissions === 'app01_admin') {
              this.isapp01_admin = true;
              this.bus.$emit('isapp01_admin', true)
              console.log('checkuser', this.isapp01_admin)
            } else if (has_permissions === 'cmdb_admin') {
              this.iscmdb_admin = true;
              this.bus.$emit('iscmdb_admin', true)
              console.log('checkuser', this.iscmdb_admin)
            }
          }
        }
      },
      handleCommand(command) {
        if (command === 'logout') {
          this.logout()
        }
        if (command === 'myself') {
          this.myself()
        }
        if (command === 'permission_manage') {
          this.permission_manage()
        }
      },
      logout() {
        window.localStorage.removeItem('userhashid');
        window.location = '/';
      },
      myself() {
        window.location = '/myself';
      },
      permission_manage() {
        window.location = '/permission_manage/index';
      }
    }
  }
</script>
