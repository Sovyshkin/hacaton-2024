<script>
import axios from "axios";

export default {
  components: {},
  data() {
    return {
      name: "",
      surname: "",
      email: "",
      organization_id: "1",
      category_id: "1",
      password: "",
      sec_role: "sample_role",
      error: "",
      status: 0,
      last: 0,
      success: false,
      message: "",
      user: "",
      type: "",
    };
  },
  methods: {
    async submit() {
      if (this.password && this.name) {
        let response = await axios.post(`/registration`, {
          name: this.name,
          surname: this.surname,
          phone: this.phone,
          email: this.email,
          organization_id: this.organization_id,
          category_id: this.category_id,
          password: this.password,
          sec_role: this.sec_role,
        });
        this.message = response.data.message;
        this.success = response.data.success;
        this.status = response.data.status;
        this.error = response.data.err;
        if (this.success) {
          let response = await axios.post(`/login`, {
            email: this.email,
            password: this.password,
          });
          this.token = response.data.token;
          this.success = response.data.success;
          setTimeout(() => {
            this.message = response.data.message;
          }, 1500);
          this.status = response.data.status;
          this.user = response.data.user;
        }
        setTimeout(() => {
          if (this.success) {
            this.$refs.form.reset();
            document.cookie = new String();
            document.cookie = `token=${this.token}; max-age=2419200`;
            document.cookie = `id=${this.user.id}; max-age=2419200`;
            if (this.user.sec_role == "super") {
              this.$router.push({ name: "supermenu" });
            } else if (this.user.sec_role == "admin") {
              this.$router.push({ name: "adminmenu" });
            } else {
              this.$router.push({ name: "menu" });
            }
          }
          this.message = "";
          this.success = "";
          this.status = "";
        }, 1500);
        setTimeout(() => {
          if (this.success) {
            this.$refs.form.reset();
            this.message = "";
            this.success = "";
            this.status = "";
          }
        }, 1500);
      }
    },

    get_id() {
      this.last = this.$route.query.last;
      if (!this.last) {
        this.category_id = this.$route.query.category_id;
        this.organization_id = this.$route.query.organization_id;
      }
    },
  },
  mounted() {
    this.get_id();
  },
};
</script>

<template>
  <div class="container">
    <div class="image">
      <div class="form-box">
        <h2 class="title">Вход</h2>
        <div class="form">
          <div class="input-box">
            <input type="text" v-model="login" required id="email" />
            <label for="" class="email">Логин</label>
          </div>
          <div class="input-box">
            <input type="password" v-model="password" required id="password" />
            <label for="" class="password">Пароль</label>
          </div>
          <div class="sign-up">
            <button class="sign-up-btn" type="submit" id="sign-up">
              Войти
            </button>
          </div>
          <div
            v-if="status"
            :class="{ error: status == 400, success: status == 200 }"
          >
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter&family=Poppins:wght@400;500&display=swap");

*,
*:before,
*:after {
  padding: 0;
  margin: 0;
  color: black;
}

.success {
  position: absolute;
  bottom: 0%;
  width: 300px;
  text-align: center;
  padding: 10px;
  color: #a0dd75;
  z-index: 10;
}
.error {
  position: absolute;
  bottom: 0%;
  width: 300px;
  text-align: center;
  padding: 10px;
  color: #dd7575;
  z-index: 10;
}

.container {
  position: relative;
  max-width: 350px;
  width: 100%;
  height: 60vh;
  background: rgba(0, 0, 0.75);
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-inline: 32px;
  overflow: hidden;
  margin: 0 auto;
}

.container::before {
  content: "";
  z-index: 0;
  position: absolute;
  height: 770px;
  width: 770px;
  background: conic-gradient(
    transparent,
    transparent,
    transparent,
    #d400d4 /* transparent, transparent, transparent, #FF1D15 */
  );
  animation: animate 4s linear infinite;
  animation-delay: -2s;
}
.container::after {
  content: "";
  z-index: 0;
  position: absolute;
  height: 770px;
  width: 770px;
  background: conic-gradient(transparent, transparent, transparent, #ff1d15);
  /* #00cfff  F18904*/
  animation: animate 4s linear infinite;
}

@keyframes animate {
  0% {
    transform: rotate(0);
  }
  0% {
    transform: rotate(360deg);
  }
}

.image {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  inset: 5px;
  background-color: #f7ede8;
  z-index: 1;
  border-radius: 16px;
}

.form-box {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  min-height: 60vh;
  gap: 30px;
}

.form-box-2 {
  min-height: 60vh;
}

.form-box-2 .form h2 {
  font-size: 32px;
  color: black;
  text-align: center;
}

.form-box .form h2 {
  font-size: 32px;
  /* color: #fff; */
  text-align: center;
}

.form .input-box {
  position: relative;
  width: 100%;
  border-bottom: 2px solid black;
}

.input-box input {
  width: 100%;
  height: 50px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 16px;
  padding: 0 35px 0 5px;
  /* color: #fff; */
}
input:focus ~ label,
input:valid ~ label {
  top: 4px;
}

.input-box label {
  position: absolute;
  /* color: #fff; */
  top: 68%;
  left: 5px;
  transform: translateY(-50%);
  font-size: 16px;
  pointer-events: none;
  transition: all 400ms ease;
}

.d-none {
  display: none;
}

.group {
  width: 100%;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.node {
  position: relative;
  top: -15px;
  color: #a71d31;
  background-color: transparent;
  text-decoration: none;
  border: none;
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
}

.sign-in {
  padding: 7px 9px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  outline: none;
  border: none;
  border-radius: 5px;
  background-color: #a71d31;
}

.sign-up-btn {
  padding: 12px 24px;
  border: 2px solid black;
  border-radius: 8px;

  transition: all 400ms;
}

.sign-up-btn:hover {
  color: #fff;
  background-color: black;
}

.sign-up-btn:focus {
  /* color: #fff; */
  background-color: #0c1022;
  border: 2px solid #fff;
}

.sign-up {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 15px 0;
}

.disabled {
  pointer-events: none;
  opacity: 0.4;
}

.form {
  display: grid;
  gap: 10px;
}

.a-back {
  text-decoration: none;
  color: #ff8200;
  text-align: center;
}

.invalid {
  text-align: center;
  border: 2px solid red;
  color: red;
  padding: 10px;
  border-radius: 10px;
}

.title {
  font-size: 30px;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  -webkit-background-clip: text;
  -webkit-text-fill-color: #ffffff;
  transition: background-color 5000s ease-in-out 0s;
  box-shadow: inset 0 0 20px 20px #23232329;
}

.wrap-radio {
  margin: 0 auto;
  display: flex;
  gap: 10px;
}

.wrap-radio button {
  padding: 12px 24px;
  border: 2px solid black;
  border-radius: 8px;

  transition: all 400ms;
}

.wrap-radio button:hover {
  color: #fff;
  background-color: black;
}

@media (max-width: 700px) {
  .container {
    height: 560px;
  }
}
</style>
