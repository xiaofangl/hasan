<template>
  <hs-layout_auto>
    <div class="main-tabs">

      <div>
        <table>
          <thead>
          <tr>
            <td>name-名称</td>
            <td>fullname-全名</td>
            <td>color</td>
            <td>url</td>
            <td>_class</td>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in res">
            <td>{{item.name}}</td>
            <td>{{item.fullname}}</td>
            <td>{{item.color}}</td>
            <td>{{item.url}}</td>
            <td>{{item._class}}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </hs-layout_auto>

</template>

<script>
  export default {
    data () {
      return {
        res: '999'
      }
    },
    activated: function () {
      this.getCaptcha();
    },
    methods: {
      getCaptcha() {
        this.$http.get(this.jks_api + 'get_all_job').then((resp) => {
          console.log('this resp', resp)
          this.res = resp.data.data;

        }).catch((error) => {
          this.res = 'error'
          console.log(this.res)
        })
      }
    }
  }
</script>
