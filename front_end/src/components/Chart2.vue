<template>
  <div>
    <div class="Echarts">
      <div id="echart2" style="width: 100%; height: 400px"></div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["homeFlag", "tableData"],
  name: "Chart2",
  data() {
    return {
      flag: true,
      myChart: {},
      option: {},
      oldata: [
        { value: 1048, name: "Normal" },
        { value: 735, name: "Active_Wiretap" },
        { value: 580, name: "ARP_MitM" },
        { value: 484, name: "Fuzzing" },
        { value: 300, name: "Mirai" },
        { value: 300, name: "OS_Scan" },
        { value: 300, name: "SSDP_Flood" },
        { value: 300, name: "SSL_Renegotiation" },
        { value: 300, name: "SYN_DoS" },
        { value: 300, name: "Video_Injection" },
      ],
    };
  },
  mounted() {
    this.myChart = this.$echarts.init(document.getElementById("echart2"));
    this.updateEcharts();
  },
  methods: {
    updateEcharts() {
      this.option = {
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: "#fff",
              borderWidth: 2,
            },
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "40",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: this.oldata,
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
      let arr = this.tableData;
      for (let i = 0; i < this.oldata.length; i++) {
        this.oldata[i].value = 0;
      }
      let labelSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
      for (let i = 0; i < this.tableData.length; i++) {
        this.oldata[this.tableData[i]].value++;
      }
      this.updateEcharts();
    },
  },
};
</script>

<style  scope>
</style>