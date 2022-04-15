<template>
  <div>
    <div class="Echarts">
      <div id="echart1" style="width: 100%; height: 400px"></div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['homeFlag', 'tableData'],
  name: "Chart1",
  data() {
    return {
      flag: true,
      myChart: {},
      option: {},
      oldata: {
        status: 1,
        type: "data",
        x: [1, 2, 3, 4, 5],
        y: [0, 0, 0, 0, 0],
      }, //贾克斯返回的数据
    };
  },
  mounted() {
    this.myChart = this.$echarts.init(document.getElementById("echart1"));
    this.updateEcharts();
  },
  methods: {
    updateEcharts() {
      // 指定图表的配置项和数据
      this.option = {
        title: {
          text: "Flow Type",
        },
        tooltip: {},
        legend: {
          data: ["Type"],
        },
        xAxis: {
          data: this.oldata.x,
        },
        yAxis: {
          scale: true,
          minInterval: 1,
        },
        series: [
          {
            name: "Type",
            type: "line",
            data: this.oldata.y,
          },
        ],
      };
      // 使用刚指定的配置项和数据显示图表。
      this.myChart.setOption(this.option);
    },
  },
  watch: {
    homeFlag(newVal, oldVal) {
      if (newVal != oldVal) {
        this.flag = newVal;
      }
    },
    // tableData: {
    //   handler(newVal, oldVal) {
    //     console.log(newVal, oldVal);
    //   },
    //   deep: true,
    // },
    flag() {
      this.oldata.x = [];
      this.oldata.y = [];
      
      for(let i = 0; i < this.tableData.length; i++){
        this.oldata.x.push(i + 1);
      }
      this.oldata.y = this.tableData;
      this.updateEcharts();
      // this.myChart = this.$echarts.init(document.getElementById("echart1"));
      // this.updateEcharts();
    },
  },
};
</script>

<style  scope>
</style>