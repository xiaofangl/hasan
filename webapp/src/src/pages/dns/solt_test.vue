<template>
  <hs-layout_auto>
    <div class="main-tabs">
      {{ 'this is solt test' }}
    </div>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span style="color: #149C4C; font-weight: 700; font-size: 16px">192_huashenghaoche.com.zone</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="add_item('ninem')">添加解析</el-button>
      </div>
      <div class="text item">
        <el-table :data="ninem" style="width: 100%" height="250">
          <el-table-column prop="type" label="记录类型" width="130">
          </el-table-column>
          <el-table-column prop="host" label="主机记录" width="170">
          </el-table-column>
          <el-table-column prop="ns_path" label="解析线路" width="120">
          </el-table-column>
          <el-table-column prop="value" label="记录值" width="180">
          </el-table-column>
          <el-table-column prop="mx" label="MX优先级" width="120">
          </el-table-column>
          <el-table-column prop="ttl" label="TTL值" width="120">
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>

            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>


    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span style="color: #149C4C; font-weight: 700; font-size: 16px">192_huashenghaoche.net.zone</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="add_item('ninet')">添加解析</el-button>
      </div>
      <div class="text item">
        <el-table :data="ninet" style="width: 100%" height="250">
          <el-table-column prop="type" label="记录类型" width="130">
          </el-table-column>
          <el-table-column prop="host" label="主机记录" width="170">
          </el-table-column>
          <el-table-column prop="ns_path" label="解析线路" width="120">
          </el-table-column>
          <el-table-column prop="value" label="记录值" width="180">
          </el-table-column>
          <el-table-column prop="mx" label="MX优先级" width="120">
          </el-table-column>
          <el-table-column prop="ttl" label="TTL值" width="120">
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>

            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>


    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span style="color: #149C4C; font-weight: 700; font-size: 16px">192_huashenghaoche.work.zone</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="add_item('ninek')">添加解析</el-button>
      </div>
      <div class="text item">
        <el-table :data="ninek" style="width: 100%" height="250">
          <el-table-column prop="type" label="记录类型" width="130">
          </el-table-column>
          <el-table-column prop="host" label="主机记录" width="170">
          </el-table-column>
          <el-table-column prop="ns_path" label="解析线路" width="120">
          </el-table-column>
          <el-table-column prop="value" label="记录值" width="180">
          </el-table-column>
          <el-table-column prop="mx" label="MX优先级" width="120">
          </el-table-column>
          <el-table-column prop="ttl" label="TTL值" width="120">
          </el-table-column>
          <el-table-column prop="status" label="状态" width="120">
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template slot-scope="scope">
              <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>

            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </hs-layout_auto>
</template>
