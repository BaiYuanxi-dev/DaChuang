<template>
  <div class="signcontainer">
    <!-- <Row :gutter="16">
      <Col :xs="8" :sm="8" :md="3" :lg="5" :xl="3">
        <el-dialog :visible.sync="dialogVisible" height="480" :before-close="handleClose">
          <el-divider />
          <video id="video" class="test" controls height="480" poster="../assets/img/img-1.jpg">
            <source src="../assets/video/T20210340_3_00223dc0.mp4" type="video/mp4" />
          </video>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
          </span>
        </el-dialog>
      </Col>
    </Row> -->

    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
      <path
        fill="#0099ff"
        fill-opacity="1"
        d="M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
      />
    </svg>
    <div class="user">
      <i class="fa fa-user"></i>
      <div ref="head" class="head">account login</div>
    </div>
    <div class="container">
      <div ref="login" class="box login">
        <div class="form-content">
          <div class="avtar">
            <div class="pic">
              <img src="../assets/img/img-l-1.jpg" alt />
            </div>
          </div>
          <h1>Welcome back</h1>
          <el-form
            :model="ruleForm"
            status-icon
            :rules="rules"
            ref="ruleForm"
            class="form"
          >
            <el-form-item prop="username">
              <el-input
                prefix-icon="el-icon-user-solid"
                v-model="ruleForm.username"
                placeholder="email"
              ></el-input>
            </el-form-item>
            <el-form-item prop="pass">
              <el-input
                prefix-icon="el-icon-lock"
                type="password"
                v-model="ruleForm.pass"
                autocomplete="off"
                placeholder="password"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                @click="submitForm('ruleForm')"
                class="custom-btn btn-3"
                >登录</el-button
              >
            </el-form-item>
          </el-form>

          <p class="btn-something">
            Don't have an account ?
            <span ref="tosignup" class="signupbtn" @click="toSignup"
              >signup</span
            >
          </p>
        </div>
      </div>
      <div ref="signup" class="box signup">
        <div class="form-content">
          <div class="avtar">
            <div class="pic">
              <img src="../assets/img/img-l-2.jpg" alt />
            </div>
          </div>
          <h1>Let's get started</h1>
          <el-form
            :model="registRuleForm"
            status-icon
            :rules="rules2"
            ref="registRuleForm"
            class="form"
          >
            <el-form-item prop="username">
              <el-input
                prefix-icon="el-icon-user-solid"
                v-model="registRuleForm.username"
                placeholder="username"
              ></el-input>
            </el-form-item>
            <el-form-item prop="pass">
              <el-input
                prefix-icon="el-icon-lock"
                type="password"
                v-model="registRuleForm.pass"
                autocomplete="off"
                placeholder="password"
              ></el-input>
            </el-form-item>
            <el-form-item prop="checkPass">
              <el-input
                prefix-icon="el-icon-lock"
                type="password"
                v-model="registRuleForm.checkPass"
                autocomplete="off"
                placeholder="repeat_password"
              ></el-input>
            </el-form-item>

            <el-form-item>
              <!-- <button class="custom-btn btn-3"><span>Read More</span></button> -->
              <el-button
                type="primary"
                @click="submitRegisterForm('registRuleForm')"
                class="custom-btn btn-3"
                >注册</el-button
              >
            </el-form-item>
          </el-form>
          <p class="btn-something">
            Already have an account ?
            <span ref="tosignin" class="loginbtn" @click="toSignin">login</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
//引入验证组件
// import api from '../axios.js'
export default {
  name: "Login",
  data() {
    var checkusername = (rule, value, callback) => {
      if (value === "") {
        return callback(new Error("邮箱不能为空"));
      }
      setTimeout(() => {
        if (!this.isEmail(value)) {
          callback(new Error("请输入正确的邮箱"));
        } else {
          callback();
        }
      }, 1000);
    };
    var validatePass0 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (value.length < 6) {
          callback(new Error("密码不少于6位"));
        }
        callback();
      }
    };
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.registRuleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.registRuleForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      dialogVisible: true,
      ruleForm: {
        pass: "",
        username: "",
      },
      rules: {
        pass: [{ validator: validatePass0, trigger: "blur" }],
        username: [{ validator: checkusername, trigger: "blur" }],
      },
      registRuleForm: {
        pass: "",
        checkPass: "",
        username: "",
      },
      rules2: {
        pass: [{ validator: validatePass, trigger: "blur" }],
        checkPass: [{ validator: validatePass2, trigger: "blur" }],
        username: [{ validator: checkusername, trigger: "blur" }],
      },
    };
  },
  methods: {
    isEmail(s) {
      return /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(
        s
      );
    },
    toSignup() {
      this.$refs.login.style.transform = "rotateY(180deg)";
      this.$refs.signup.style.transform = "rotateY(0deg)";
      this.$refs.head.innerHTML = "create account";
    },
    toSignin() {
      this.$refs.login.style.transform = "rotateY(0deg)";
      this.$refs.signup.style.transform = "rotateY(-180deg)";
      this.$refs.head.innerHTML = "account login";
    },

    submitForm(formName) {
      this.$router.push({ path: "/Home" });
      //提交登录表单
      if (true) {
        this.$router.push({
          name: "Home",
          query: {
            username: this.ruleForm.username,
          },
        });
      }
    },
    submitRegisterForm(formName) {
      //提交注册表单
    },
  },
};
</script>

<style scoped>
/* body {
  background-color: #f0f5f5;
} */

body::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #3399ff;
  clip-path: circle(20% at 100% 0);
}

.container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20rem;
  height: 28rem;
  perspective: 1500px;
  -webkit-perspective: 1500px;
  -moz-perspective: 1500px;
}

.box {
  position: absolute;
  top: 0;
  left: 0;
  width: 20rem;
  height: 28rem;
  border-radius: 10px;
  cursor: pointer;
  backface-visibility: hidden;
  transition: all 0.5s;
  user-select: none;
}

.signup {
  /* background-color: blue; */
  transform: rotateY(-108deg);
}

.container .form-content {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  box-shadow: 0 0 1px #3399ff;
  border-radius: 30px;
  background-color: #fff;
}

.container .form-content .avtar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.container .form-content .avtar .pic {
  position: relative;
  width: 80px;
  height: 80px;
  overflow: hidden;
  border-radius: 50%;
  border: 1px solid #3399ff;
}

.container .form-content .avtar .pic img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.container .form-content h1 {
  font-size: 1.6rem;
}

.container .form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.container .form input {
  width: 16rem;
  padding: 0.8rem;
  padding-left: 3rem;
  outline: none;
  border: none;
  border-radius: 15px;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
  margin: 5px;
}

/* .container .form div {
  position: relative;
} */

.container .form .fa {
  position: absolute;
  top: 18px;
  left: 25px;
}

.container .form .btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-top: 10px;
}

.container .form .btn button {
  text-transform: uppercase;
  padding: 8px;
  border: none;
  outline: none;
  background-color: #0066ff;
  color: #fff;
  width: 12rem;
  border-radius: 30px;
  cursor: pointer;
}

.container .btn-something {
  color: #888;
  font-size: 14px;
}

.container .btn-something span {
  color: #0066ff;
  cursor: pointer;
  font-weight: 500;
}

svg {
  position: absolute;
  bottom: 0;
  z-index: -1;
}

.user {
  position: absolute;
  top: 16rem;
  left: 5rem;
}

.user .fa-user {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 5rem;
  color: #0066ff;
}

.user .head {
  font-size: 1.6rem;
  text-transform: uppercase;
  user-select: none;
  text-shadow: 1px 1px 1px rgba(16, 16, 16, 0.1),
    1px 2px 1px rgba(16, 16, 16, 0.1), 1px 3px 1px rgba(16, 16, 16, 0.1),
    1px 4px 1px rgba(16, 16, 16, 0.1), 1px 5px 1px rgba(16, 16, 16, 0.1),
    1px 6px 1px rgba(16, 16, 16, 0.1), 1px 7px 1px rgba(16, 16, 16, 0.1),
    1px 8px 1px rgba(16, 16, 16, 0.1);
}

.custom-btn {
  width: 130px;
  height: 40px;
  color: #fff;
  border-radius: 5px;
  padding: 10px 25px;
  font-family: "Lato", sans-serif;
  font-weight: 500;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
  box-shadow: inset 2px 2px 2px 0px rgba(255, 255, 255, 0.5),
    7px 7px 20px 0px rgba(0, 0, 0, 0.1), 4px 4px 5px 0px rgba(0, 0, 0, 0.1);
  outline: none;
}

.btn-3 {
  background: rgb(0, 172, 238);
  background: linear-gradient(
    0deg,
    rgba(0, 172, 238, 1) 0%,
    rgba(2, 126, 251, 1) 100%
  );
  width: 130px;
  height: 40px;
  line-height: 42px;
  padding: 0;
  border: none;
}

.btn-3 span {
  position: relative;
  display: block;
  width: 100%;
  height: 100%;
}

.btn-3:before,
.btn-3:after {
  position: absolute;
  content: "";
  right: 0;
  top: 0;
  background: rgba(2, 126, 251, 1);
  transition: all 0.3s ease;
}

.btn-3:before {
  height: 0%;
  width: 2px;
}

.btn-3:after {
  width: 0%;
  height: 2px;
}

.btn-3:hover {
  background: transparent;
  box-shadow: none;
}

.btn-3:hover:before {
  height: 100%;
}

.btn-3:hover:after {
  width: 100%;
}

.btn-3 span:hover {
  color: rgba(2, 126, 251, 1);
}

.btn-3 span:before,
.btn-3 span:after {
  position: absolute;
  content: "";
  left: 0;
  bottom: 0;
  background: rgba(2, 126, 251, 1);
  transition: all 0.3s ease;
}

.btn-3 span:before {
  width: 2px;
  height: 0%;
}

.btn-3 span:after {
  width: 0%;
  height: 2px;
}

.btn-3 span:hover:before {
  height: 100%;
}

.btn-3 span:hover:after {
  width: 100%;
}
.test {
  width: 100%;
}
</style>