<template>
  <hs-layout_auto>
    <div style="padding-top: 50px;">
      <div class="main-tabs">
        <div style="width: 69%; padding-left: 40px;">
          <el-form ref="form" :model="sizeForm" label-width="80px" size="mini">
            <el-form-item label="文件名称">
              <el-input v-model="sizeForm.name"></el-input>
            </el-form-item>
            <el-form-item label="创建主机">
              <el-select v-model="sizeForm.region" placeholder="请选择创建主机">
                <el-option label="主机1" value="shanghai"></el-option>
                <el-option label="主机2" value="beijing"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="同步文件">
              <el-col :span="11">
                <el-date-picker type="date" placeholder="选择zone文件" v-model="sizeForm.date1"
                                style="width: 100%;"></el-date-picker>
              </el-col>
              <el-col class="line" :span="2">-</el-col>
              <el-col :span="11">
                <el-time-picker type="fixed-time" placeholder="选择主机ip" v-model="sizeForm.date2"
                                style="width: 100%;"></el-time-picker>
              </el-col>
            </el-form-item>
            <el-form-item label="活动性质">
              <el-checkbox-group v-model="sizeForm.type">
                <el-checkbox-button label="美食/餐厅线上活动" name="type"></el-checkbox-button>
                <el-checkbox-button label="地推活动" name="type"></el-checkbox-button>
                <el-checkbox-button label="线下主题活动" name="type"></el-checkbox-button>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="特殊资源">
              <el-radio-group v-model="sizeForm.resource" size="medium">
                <el-radio border label="线上品牌商赞助"></el-radio>
                <el-radio border label="线下场地免费"></el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item size="large">
              <el-button type="primary" @click="onSubmit">立即创建</el-button>
              <el-button>取消</el-button>
            </el-form-item>
          </el-form>
        </div>

      </div>
    </div>
  </hs-layout_auto>
</template>

<script>
  export default {
    data() {
      return {
        sizeForm: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        }
      };
    },
    methods: {
      onSubmit() {
        console.log('submit!');
      }
    }
  };
</script>
<style>
  .el-form {
    background-color: white;
    padding: 50px;
    width: 70rem;
    border: 1px solid rgb(191, 217, 204);
  }

  .el-input__inner {
    border-style: solid;
    border-radius: 4px;
    border: 1px solid rgb(191, 217, 204);
  }
</style>
