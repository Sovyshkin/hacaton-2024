<script>
import axios from "axios";
export default {
  name: "AppHeader",
  components: {},
  data() {
    return {
      target: 0,
      id: this.getCookieValue("id"),
      vuz: "",
      adminvuz: false,
      vuzid: "",
    };
  },
  methods: {
    gotolog() {
      this.$router.push({ name: "log" });
    },
    gotoreg() {
      this.$router.push({ name: "reg" });
    },
    goHome() {
      this.$router.push({ name: "home" });
    },
    async goVuz() {
      this.id = this.getCookieValue("id");
      if (this.id) {
        let response = await axios.post(`/info-profile`, {
          params: {
            id: this.id,
          },
        });
        if (response.data.typeuser == "создатель вуза") {
          let res = await axios.post(`/get_vuz`, {
            params: {
              userid: this.id,
              namevuz: "False",
              id: "False",
            },
          });
          console.log("id", res.data.id);
          this.$router.push({
            name: "vuz",
            query: { id: res.data.id, edit: true },
          });
        } else {
          this.$router.push({
            name: "reg",
            query: {
              type: "vuz",
            },
          });
        }
      } else {
        this.$router.push({
          name: "reg",
          query: {
            type: "vuz",
            query: { id: this.vuzid },
          },
        });
      }
    },
    goStudent() {
      this.$router.push({ name: "reg" });
    },
    goPred() {
      this.$router.push({ name: "reg" });
    },
    getCookieValue(name) {
      const cookies = document.cookie.split("; ");
      let res;
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        if (cookie.slice(0, 2) == name) {
          res = cookie.replace(name + "=", "");
        }
      }
      return res;
    },
    async getUser() {
      let response = await axios.post(`/info-profile`, {
        params: {
          id: this.getCookieValue("id"),
        },
      });
      let type = response.data.typeuser;
      if (type == "создатель вуза") {
        this.adminvuz = true;
        let res = await axios.post(`/get_vuzid`, {
          params: {
            id: this.getCookieValue("id"),
          },
        });
        this.vuzid = res.data.vuzid;
        this.$router.push({ name: "vuz", query: { id: this.vuzid } });
      }
    },
  },
  mounted() {
    this.getUser();
  },
};
</script>
<template>
  <div class="wrap-header">
    <div class="nav" v-if="!target">
      <div @click="goHome" class="logo">
        <img src="@/assets/LOGO.png" alt="Лого" />
      </div>
      <div @click="goVuz" v-if="!id" class="nav-item nav-small">ВУЗам</div>
      <div @click="goPred" v-if="!id" class="nav-item nav-small">
        Предприятиям
      </div>
      <div
        @click="this.$router.push({ name: 'lenta' })"
        v-if="id"
        class="nav-item nav-small"
      >
        Лента
      </div>
      <div
        @click="this.$router.push({ name: 'events' })"
        v-if="id"
        class="nav-item nav-small"
      >
        Мероприятия
      </div>
      <div @click="getUser" v-if="adminvuz" class="nav-item nav-small">
        Мой ВУЗ
      </div>
      <div @click="goStudent" v-if="!id" class="nav-item nav-small">
        Студентам
      </div>
    </div>
    <div class="auth" v-if="!id">
      <button @click="gotolog" class="btn btn-log">Вход</button>
      <button @click="gotoreg" class="btn btn-reg">Регистрация</button>
    </div>
    <div class="auth" v-if="id">
      <img
        src="@/assets/user.png"
        @click="this.$router.push({ name: 'profile' })"
        class="user"
      />
    </div>
    <div class="auth-small" @click="this.target = !this.target">
      <div v-if="target" class="nav-item">О нас</div>
      <div v-if="target" class="nav-item">Больше</div>
      <button v-if="target" @click="gotolog" class="btn btn-log small">
        Вход
      </button>
      <button v-if="target" @click="gotoreg" class="btn btn-reg small">
        Регистрация
      </button>
      <img src="@/assets/threeLine.png" alt="" />
    </div>
  </div>
</template>
<style scoped>
.wrap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav {
  display: flex;
  gap: 30px;
  align-items: center;
}

.nav-item {
  font-size: 18px;
  cursor: pointer;
}

.logo img {
  height: 35px;
  cursor: pointer;
}

.user {
  cursor: pointer;
  height: 40px;
}

.btn {
  padding: 12px 24px;
  border: 2px solid black;
  border-radius: 8px;

  transition: all 400ms;
}

.btn-reg {
  color: #fff;
  background: black;
}

.btn-reg:hover {
  color: black;
  background-color: transparent;
}

.btn-log:hover {
  color: #fff;
  background-color: black;
}

.nav-item::after {
  background-color: black; /* Цвет линии при наведении на нее курсора мыши */
  display: block;
  content: "";
  height: 2px; /* Высота линии */
  width: 0%;
  -webkit-transition: width 0.3s ease-in-out;
  -moz--transition: width 0.3s ease-in-out;
  transition: width 0.3s ease-in-out;
}
.nav-item:hover:after,
.nav-item:focus:after {
  width: 100%;
}

.auth {
  display: flex;
  align-items: center;
  gap: 15px;
}

.auth-small {
  width: 100%;
  display: none;
  cursor: pointer;
  justify-content: right;
  align-items: center;
  gap: 15px;
}

.auth-small img {
  width: 30px;

  transition: all 400ms ease;
}

.small {
  border: none;
  background: transparent;
  color: black;
}

.small:hover {
  background: transparent !important;
  color: black;
}

@media (max-width: 870px) {
  .auth {
    display: none;
  }

  .nav-small {
    display: none;
  }

  .auth-small {
    display: flex;
  }

  .auth-small button {
    padding: 0;
  }
}

@media (max-width: 1000px) {
  .auth {
    gap: 5px;
  }

  .nav {
    gap: 10px;
  }
}
</style>
