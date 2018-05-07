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
    activated: function () {
      this.username = window.localStorage.getItem('username');
      // this.isAdmin = window.localStorage.getItem('is_admin');
      if (window.localStorage.getItem('is_admin') === 'true') {
        this.isAdmin = 1;
      }
      // console.log('header', this.username, this.isAdmin, window.localStorage.getItem('is_admin'))
    },

    methods: {
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
