<template>
  <el-card class="box-card">
    <el-empty v-if="flag">
      <input
        type="file"
        id="files"
        ref="refFile"
        style="display: none"

        v-on:change="fileLoad"
      />
    </el-empty>
    <el-table v-else :data="tableData" stripe style="width: 100%" height="600">
      <el-table-column prop="id" label="Flow" width="250"> </el-table-column>
      <el-table-column prop="type" label="Type" width="250"> </el-table-column>
    </el-table>
    <div style="margin-left: 150px">
      <el-button
        v-loading.fullscreen.lock="loading"
        type="primary"
        id="fileImport"
        v-on:click="clickLoad"
        style="height: 60px; width: 200px; font-size: 20px "
      >
      {{butName}}
    </el-button>
    <!-- <el-button
        v-else
        type="primary"
        id="fileImport"
        v-on:click="clickLoad"
        style="height: 60px; width: 200px; font-size: 20px "
      >
      重新导入
    </el-button> -->
    </div>
    
  </el-card>
</template>

<script>
export default {
  props: {
    homeFlag: Number,
  },
  name: "LeftTab",
  data() {
    return {
      butName: "导入数据",
      flag: true,
      arr: [],
      tableData: [
        {
          id: 1,
          type: "王小虎",
        },
        {
          id: 2,
          type: "王小虎",
        },
        {
          id: 3,
          type: "王小虎",
        },
        {
          id: 4,
          type: "王小虎",
        },
      ],
      loading:false,
    };
  },
  methods: {
    // getData() {
    //   let files = event.target.files[0];
    // },
    clickLoad() {
      this.flag = true;
      if(this.homeFlag % 3 == 0){
        this.loading = true;
      }
      console.log(this.homeFlag)
      
      this.$emit("changeHomeFlag", this.homeFlag + 1);
      this.$refs.refFile.dispatchEvent(new MouseEvent("click"));
    },
    fileLoad() {
      //获取读取的文件File对象 下面两种方法实现效果一样
      //方法一:原生html获取
      // const selectedFile = document.getElementById('files').files[0];
      //方法二:Vue实现
      const selectedFile = this.$refs.refFile.files[0];
      // console.log(selectedFile);
      var name = selectedFile.name; //选中文件的文件名
      var size = selectedFile.size; //选中文件的大小
      // console.log("文件名:" + name + "大小:" + size);
      this.getData(name);
    },
    getData(filename) {
      var that = this;
      // 对应 Python 提供的接口，这里s的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      let path = "http://127.0.0.1:5000/";
      switch(filename){
        case "test1.pcap":
          path +="getMsg1";
          break;
        case "test2.pcap":
          path +="getMsg2";
          break;
        case "data.pcap":
          path +="getMsg3";
          break;
      }
      this.$ajax.get(path).then(function (response) {
        // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
        // 可以直接通过 response.data 取key-value
        // 坑一：这里不能直接使用 this 指针，不然找不到对象
        var msg = response.data.msg;
        // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
        that.arr = msg;
        that.setTable(msg);
        that.flag = false;
        that.$emit("changeHomeFlag", that.homeFlag + 1);
        that.loading = false;
        // that.$emit('')
      });
      // .catch(function (error) {
      //   alert("Error " + error);
      // });
      // this.$ajax
      //   // .post(
      //   //   path,
      //   //   {
      //   //     file: filename,
      //   //   },
      //   //   { emulateJSON: true },
      //   //   {
      //   //     // 这里是跨域写法
      //   //     headers:{"Access-Control-Allow-Origin": "*"}, // 这里是跨域的写法
      //   //   }
      //   // )
      //   .get(path)
      //   .then((response) => {
      //     var msg = response.data.msg;
      //     // // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
      //     that.arr = msg;
      //     that.setTable(msg);
      //     that.flag = false;
      //     that.$emit("changeHomeFlag", that.homeFlag + 1);
      //     // console.log(that.$refs.refFile.value);
      //     that.$refs.refFile.value = null;
      //   });
        // this.$refs.refFile[0].values = null;
    },

    setTable(msg) {
      let type = "";
      this.tableData = [];
      for (let i = 0; i < msg.length; i++) {
        let element = {
          id: 0,
          type: "",
        };
        switch (msg[i]) {
          case 0:
            type = "Normal";
            break;
          case 1:
            type = "Active_Wiretap";
            break;
          case 2:
            type = "ARP_MitM";
            break;
          case 3:
            type = "Fuzzing";
            break;
          case 4:
            type = "Mirai";
            break;
          case 5:
            type = "OS_Scan";
            break;
          case 6:
            type = "SSDP_Flood";
            break;
          case 7:
            type = "SSL_Renegotiation";
            break;
          case 8:
            type = "SYN_DoS";
            break;
          case 9:
            type = "Video_Injection";
            break;
        }
        element.id = i + 1;

        element.type = type;
        // console.log(element);
        this.tableData.push(element);
      }
      this.butName = "重新导入"

    },

    tableToHome() {
      return this.arr;
    },
  },
};
</script>

<style scope>
</style>