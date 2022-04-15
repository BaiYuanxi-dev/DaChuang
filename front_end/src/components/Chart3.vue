<template>
  <div>
    <div class="Echarts">
      <div id="echart3" style="width: 100%; height: 400px"></div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["homeFlag", "tableData"],
  name: "Chart3",
  data() {
    return {
      flag: true,
      myChart: {},
      option: {},
      valOnRadianMax: 200, //数据大小
      normalData: 0,
      panelImageURL: "@/assets/custom-gauge-panel.png",

      outerRadius: 200,
      innerRadius: 170,
      pointerInnerRadius: 40,
      insidePanelRadius: 140,
      currentDataIndex: 0,
    };
  },
  mounted() {
    this.myChart = this.$echarts.init(document.getElementById("echart3"));
    this.updateEcharts();
  },
  methods: {
    updateEcharts() {
      var _animationDuration = 1000;
      var _animationDurationUpdate = 1000;
      var _animationEasingUpdate = "quarticInOut";
      this.option = {
        title: {
          text: "Normal Flow",
        },
        animationEasing: _animationEasingUpdate,
        animationDuration: _animationDuration,
        animationDurationUpdate: _animationDurationUpdate,
        animationEasingUpdate: _animationEasingUpdate,
        dataset: {
          source: [[1, this.normalData]], //对应前面的max
        },
        tooltip: {},
        angleAxis: {
          type: "value",
          startAngle: 0,
          show: false,
          min: 0,
          max: this.valOnRadianMax,
        },
        radiusAxis: {
          type: "value",
          show: false,
        },
        polar: {},
        series: [
          {
            type: "custom",
            coordinateSystem: "polar",
            renderItem: this.renderItem,
          },
        ],
      };
      //   setInterval(function () {
      //     var nextSource = [[1, this.normalData]];
      //     this.myChart.setOption({
      //       dataset: {
      //         source: nextSource,
      //       },
      //     });
      //   }, 3000);
      this.myChart.setOption(this.option);
    },

    renderItem(params, api) {
      var that = this;
      var valOnRadian = api.value(1);
      var coords = api.coord([api.value(0), valOnRadian]);
      var polarEndRadian = coords[3];
      var imageStyle = {
        image: require("@/assets/custom-gauge-panel.png"),
        x: params.coordSys.cx - this.outerRadius,
        y: params.coordSys.cy - this.outerRadius,
        width: this.outerRadius * 2,
        height: this.outerRadius * 2,
      };
      return {
        type: "group",
        children: [
          {
            type: "image",
            style: imageStyle,
            clipPath: {
              type: "sector",
              shape: {
                cx: params.coordSys.cx,
                cy: params.coordSys.cy,
                r: this.outerRadius,
                r0: this.innerRadius,
                startAngle: 0,
                endAngle: -polarEndRadian,
                transition: "endAngle",
                enterFrom: { endAngle: 0 },
              },
            },
          },
          {
            type: "image",
            style: imageStyle,
            clipPath: {
              type: "polygon",
              shape: {
                points: this.makePionterPoints(params, polarEndRadian),
              },
              extra: {
                polarEndRadian: polarEndRadian,
                transition: "polarEndRadian",
                enterFrom: { polarEndRadian: 0 },
              },
              during: function (apiDuring) {
                apiDuring.setShape(
                  "points",
                  that.makePionterPoints(
                    params,
                    apiDuring.getExtra("polarEndRadian")
                  )
                );
              },
            },
          },
          {
            type: "circle",
            shape: {
              cx: params.coordSys.cx,
              cy: params.coordSys.cy,
              r: this.insidePanelRadius,
            },
            style: {
              fill: "#fff",
              shadowBlur: 25,
              shadowOffsetX: 0,
              shadowOffsetY: 0,
              shadowColor: "rgba(76,107,167,0.4)",
            },
          },
          {
            type: "text",
            extra: {
              valOnRadian: valOnRadian,
              transition: "valOnRadian",
              enterFrom: { valOnRadian: 0 },
            },
            style: {
              text: this.makeText(valOnRadian),
              fontSize: 50,
              fontWeight: 700,
              x: params.coordSys.cx,
              y: params.coordSys.cy,
              fill: "rgb(0,50,190)",
              align: "center",
              verticalAlign: "middle",
              enterFrom: { opacity: 0 },
            },
            during: function (apiDuring) {
              apiDuring.setStyle(
                "text",
                that.makeText(apiDuring.getExtra("valOnRadian"))
              );
            },
          },
        ],
      };
    },
    convertToPolarPoint(renderItemParams, radius, radian) {
      return [
        Math.cos(radian) * radius + renderItemParams.coordSys.cx,
        -Math.sin(radian) * radius + renderItemParams.coordSys.cy,
      ];
    },
    makePionterPoints(renderItemParams, polarEndRadian) {
      return [
        this.convertToPolarPoint(
          renderItemParams,
          this.outerRadius,
          polarEndRadian
        ),
        this.convertToPolarPoint(
          renderItemParams,
          this.outerRadius,
          polarEndRadian + Math.PI * 0.03
        ),
        this.convertToPolarPoint(
          renderItemParams,
          this.pointerInnerRadius,
          polarEndRadian
        ),
      ];
    },
    makeText(valOnRadian) {
      var that = this;
      // Validate additive animation calc.
      if (valOnRadian < -10) {
        alert("illegal during val: " + valOnRadian);
      }
      return ((valOnRadian / this.valOnRadianMax) * 100).toFixed(0) + "%";
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
      this.normalData = 0;
      for (let i = 0; i < this.tableData.length; i++) {
          if(this.tableData[i] == 0){
              this.normalData ++;
          }
      }
      this.valOnRadianMax = this.tableData.length;
      //   this.oldata.y = this.tableData;

      console.log(this.tableData);
      this.updateEcharts();
    },
  },
};
</script>

<style>
</style>