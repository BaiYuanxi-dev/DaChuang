<template>
  <div>
    <div class="Echarts">
      <div id="echart4" style="width: 100%; height: 400px"></div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["homeFlag", "tableData"],
  name: "Chart4",
  data() {
    return {
      flag: true,
      myChart: {},
      option: {},
      //   oldata: {
      //     status: 1,
      //     type: "data",
      //     x: [1, 2, 3, 4, 5],
      //     y: [0, 0, 0, 0, 0],
      //   }, //贾克斯返回的数据
    };
  },
  mounted() {
    this.myChart = this.$echarts.init(document.getElementById("echart4"));
    this.updateEcharts();
  },
  methods: {
    updateEcharts() {
      this.option = {
        tooltip: {
          trigger: "item",
          triggerOn: "mousemove",
        },
        animation: false,
        series: [
          {
            type: "sankey",
            bottom: "10%",
            emphasis: {
              focus: "adjacency",
            },
            data: [
              { name: "a" },
              { name: "b" },
              { name: "a1" },
              { name: "b1" },
              { name: "c" },
              { name: "e" },
            ],
            links: [
              { source: "a", target: "a1", value: 5 },
              { source: "e", target: "b", value: 3 },
              { source: "a", target: "b1", value: 3 },
              { source: "b1", target: "a1", value: 1 },
              { source: "b1", target: "c", value: 2 },
              { source: "b", target: "c", value: 1 },
            ],
            orient: "vertical",
            label: {
              position: "top",
            },
            lineStyle: {
              color: "source",
              curveness: 0.5,
            },
          },
        ],
      };
      this.myChart.setOption(this.option);
    },
  },
  watch: {
    homeFlag(newVal, oldVal) {
      if (newVal != oldVal) {
        this.flag = newVal;
      }
    },
    flag() {
      //   this.oldata.x = [];
      //   this.oldata.y = [];

      //   for (let i = 0; i < this.tableData.length; i++) {
      //     this.oldata.x.push(i + 1);
      //   }
      //   this.oldata.y = this.tableData;
      this.updateEcharts();
      // this.myChart = this.$echarts.init(document.getElementById("echart1"));
      // this.updateEcharts();
    },
  },
};
</script>

<style>
</style>