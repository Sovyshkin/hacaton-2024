<script>
import axios from "axios";

export default {
  components: {},
  data() {
    return {
      name: "",
      surname: "",
      email: "",
      password: "",
      sec_role: "sample_role",
      error: "",
      status: 0,
      last: 0,
      success: false,
      message: "",
      user: "",
      type: "",
      id: "",
    };
  },
  methods: {
    async submit() {
      let response;
      if (this.password && this.name && this.type == "student") {
        response = await axios.post(`/registration-prof`, {
          params: {
            login: this.login,
            password: this.password,
            nameprof: this.name,
            surnameprof: this.surname,
          },
        });
      } else if (this.password && this.name && this.type == "vuz") {
        response = await axios.post(`/registration-profvuz`, {
          params: {
            login: this.login,
            password: this.password,
            nameprof: this.name,
            surnameprof: this.surname,
          },
        });
      }
      this.message = response.data.message;
      this.status = response.data.status;
      this.id = response.data.id;

      setTimeout(() => {
        document.cookie = new String();
        document.cookie = `id=${this.id}; max-age=2419200`;
        this.message = "";
        this.status = "";
        this.$router.push({ name: "profile" });
      }, 3000);
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
  <div v-if="!type" class="wrap-radio">
    <button @click="type = 'student'">Я студент</button>
    <button @click="type = 'vuz'">Я ВУЗ</button>
  </div>
  <div v-else class="container">
    <div class="image">
      <div class="form-box">
        <h2 class="title">Регистрация</h2>
        <div class="form">
          <div class="input-box">
            <input type="text" v-model="name" required id="name" />
            <label for="" class="name">Имя</label>
          </div>
          <div class="input-box">
            <input type="text" v-model="surname" required id="surname" />
            <label for="" class="surname">Фамилия</label>
          </div>
          <div class="input-box">
            <input type="text" v-model="login" required id="email" />
            <label for="" class="email">Логин</label>
          </div>
          <div class="input-box">
            <input type="password" v-model="password" required id="password" />
            <label for="" class="password">Пароль</label>
          </div>
          <div class="sign-up">
            <button
              @click="submit"
              class="sign-up-btn"
              type="submit"
              id="sign-up"
            >
              Зарегистрировать
            </button>
          </div>
        </div>
        <div v-if="message" class="notification-container">
          <div :class="{ error: status == 400, success: status == 200 }">
            <span>{{ message }}</span>
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

input:-webkit-autofill,
textarea:-webkit-autofill,
select:-webkit-autofill {
  -webkit-box-shadow: 0 0 0px 1000px transparent inset !important;
}
.notification-container {
  position: fixed;
  bottom: 3%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.success {
  background-color: #87e752;
  border-radius: 15px;
  padding: 7px 12px;
  color: #fff;
}
.error {
  background-color: #ed1c24;
  border-radius: 15px;
  padding: 7px 12px;
  color: #fff;
  font-weight: 550;
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
  position: relative;
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
  -webkit-text-fill-color: blacks;
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
