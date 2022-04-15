<template>
  <!-- <el-container>
    <el-header>Header</el-header>
    <el-container>
      <el-aside :xs="10" :sm="10" :md="10" :lg="10" :xl="10">文</el-aside>
      <el-main :xs="14" :sm="14" :md="14" :lg="14" :xl="14">
          
      </el-main>
    </el-container>
  </el-container> -->
  <div>
    <Header></Header>
    <el-row :gutter="20">
      <el-col :xs="8" :sm="8" :md="8" :lg="8" :xl="8">
        <LeftTab
          class="heigh"
          ref="leftTab"
          :homeFlag="homeFlag"
          @changeHomeFlag="changeHomeFlag"
          :tableData="tableData"
        ></LeftTab>
        <!-- <div class="grid-content bg-purple">
            
        </div> -->
      </el-col>
      <el-col :xs="16" :sm="16" :md="16" :lg="16" :xl="16">
        <el-row>
          <Chart1 :homeFlag="homeFlag" :tableData="tableData"></Chart1>
        </el-row>
        <el-row>
          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
            <Chart2 :homeFlag="homeFlag" :tableData="tableData"></Chart2>
          </el-col>

          <el-col :xs="12" :sm="12" :md="12" :lg="12" :xl="12">
            <Chart3 :homeFlag="homeFlag" :tableData="tableData"></Chart3>
          </el-col>
          
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Chart1 from "../components/Chart1.vue";
import Chart2 from "../components/Chart2.vue";
import Chart3 from "../components/Chart3.vue";
import Chart4 from "../components/Chart4.vue"
import Header from "../components/Header.vue";
import LeftTab from "../components/LeftTab.vue";
export default {
  name: "Home",
  components: {
    Chart1,
    Chart2,
    Chart3,
    Chart4,
    Header,
    LeftTab,
  },
  data() {
    return {
      homeFlag: 0,
      tableData: [],
    };
  },

  methods: {
    /**修改tableData */
    handleEdit() {
      let tmp = this.$refs["leftTab"].tableToHome();
      this.tableData = tmp;
    },
    changeHomeFlag(value) {
      this.homeFlag = value;
    },
  },
  watch: {
    
     /**当flag值改变时修改tableData */
    homeFlag(){
      this.handleEdit();
    }
  },
};
</script>

<style scope>
html,
body {
  height: 100%;
  margin: 0px;
  padding: 0px;
}
/* .el-container {
  height: 100%;
}
.el-header{
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}
.el-aside {
  background-color: #d3d;
  color: #333;
  text-align: center;
  line-height: 200px;
}
.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
  line-height: 160px;
}
.el-menu {
  background-color: #d3dce6;
} */

.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.heigh {
  height: 100%;
}
</style>