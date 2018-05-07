/**
 * Created by xiaofangl on 2018/2/7.
 */
export default [
  // login
  {
    path: '/',
    name: '001',
    component: resolve => require(['./pages/login/index'], resolve)
  },
  {
    path: '/reset_pwd',
    name: '002',
    component: resolve => require(['./pages/login/reset_pawd'], resolve)
  },
  {
    path: '/myself',
    name: '009',
    label: '个人中心',
    component: resolve => require(['./pages/myself/index'], resolve)
  },
  {
    path: '/test01',
    name: '999',
    label: 'test01',
    component: resolve => require(['./pages/test01'], resolve)
  },
  // 权限 auth
  {
    path: '/permission_manage/index',
    name: '008',
    label: '权限管理',
    component: resolve => require(['./pages/permission_manage/index'], resolve)
  },
  // 发代码
  {
    path: '/deploy_platform/list_all_jobs',
    name: '011',
    label: 'jks_all_job',
    component: resolve => require(['./pages/deploy_platform/all_jobs'], resolve)
  },
  {
    path: '/deploy_platform/project/:id',
    name: '012',
    label: '项目信息',
    component: resolve => require(['./pages/deploy_platform/project'], resolve)
  },
  {
    path: '/deploy_platform/new_project',
    name: '012-1',
    label: '新建项目',
    component: resolve => require(['./pages/deploy_platform/new_project'], resolve)
  },
  {
    path: '/deploy_platform/deploy',
    name: '013',
    label: '发布管理',
    component: resolve => require(['./pages/deploy_platform/deploy'], resolve)
  },
  // dns_webui
  {
    path: '/dns/dns_list',
    name: '091',
    label: 'dns展示-测试',
    component: resolve => require(['./pages/dns/dns_list-test'], resolve)
  },

  // cmdb
  {
    path: '/cmdb/index',
    name: '031',
    label: '资源列表',
    component: resolve => require(['./pages/cmdb/index'], resolve)
  },
  {
    path: '/cmdb/add_item',
    name: '031-1',
    label: '新建资源',
    component: resolve => require(['./pages/cmdb/add_item'], resolve)
  },

  {
    path: '/dns/solt_test',
    name: '092',
    label: 'solt_test',
    component: resolve => require(['./pages/dns/solt_test'], resolve)
  },

  // dns_webui_link
  {
    path: '/dns/dns_oper',
    name: '021',
    label: '记录',
    component: resolve => require(['./pages/dns/dns_oper'], resolve)
  },
  {
    path: '/dns/dns_file',
    name: '022',
    label: '文件',
    component: resolve => require(['./pages/dns/dns_file'], resolve)
  }
]
