<script>
import axios from "axios";
import { defineComponent } from "vue";
// import dayjs from "dayjs";
import "dayjs/locale/ru";
import { Carousel, Navigation, Slide, Pagination } from "vue3-carousel";

import "vue3-carousel/dist/carousel.css";

export default defineComponent({
  components: {
    Carousel,
    Slide,
    Navigation,
    Pagination,
  },
  data() {
    return {
      id: "",
      img: [],
      desc: "",
      name: "",
      date: "",
      type: "",
      place: "",
      reqs: [],
      mems: [],
      message: "",
      status: "",
      users: [],
      admin: false,
      users_mems: [],
    };
  },
  methods: {
    async load_info() {
      let userid = this.getCookieValue("id");
      let res = await axios.post(`/info-profile`, {
        params: {
          id: userid,
        },
      });
      let typeuser = res.data.typeuser;
      if (typeuser == "создатель вуза") {
        this.admin = true;
      } else {
        this.admin = false;
      }
      this.id = this.$route.query.id;
      let card = await axios.post(`/get_event`, {
        params: {
          id: this.id,
        },
      });
      this.desc = card.data.desc;
      this.img = JSON.parse(card.data.img.replace(/'/g, '"'));
      this.name = card.data.name;
      this.date = card.data.date;
      this.type = card.data.type;
      this.place = card.data.place;
      this.reqs = JSON.parse(card.data.reqs.replace(/'/g, '"'));
      this.mems = JSON.parse(card.data.mems.replace(/'/g, '"'));
      if (this.reqs) {
        this.reqs.forEach(async (id) => {
          let response = await axios.post(`/info-profile`, {
            params: {
              id: id,
            },
          });
          this.users.push({
            id: id,
            name: response.data.nameprof,
            surname: response.data.surnameprof,
            img: response.data.photoprof,
          });
        });
      }
      if (this.mems) {
        this.mems.forEach(async (id) => {
          let response = await axios.post(`/info-profile`, {
            params: {
              id: id,
            },
          });
          this.users_mems.push({
            id: id,
            name: response.data.nameprof,
            surname: response.data.surnameprof,
            img: response.data.photoprof,
          });
        });
      }
    },

    async create_req() {
      let response = await axios.post(`/create_req`, {
        params: {
          userid: this.getCookieValue("id"),
          eventid: this.id,
        },
      });
      this.message = response.data.message;
      this.status = response.data.status;
      setTimeout(() => {
        this.message = "";
        this.status = "";
        location.reload();
      });
    },
    async getUser(id) {
      let response = await axios.post(`/info-profile`, {
        params: {
          id: id,
        },
      });
      let user = { name: "", surname: "" };
      user.name = response.data.nameprof;
      return user;
    },
    async confirm(id) {
      console.log(id);
      let response = await axios.post(`/set_mems`, {
        params: {
          userid: id,
          eventid: this.id,
          confirm: "True",
          typeevent: this.type,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      this.load_info();
      setTimeout(() => {
        this.status = "";
        this.message = "";
        location.reload();
      }, 3000);
    },
    async reject(id) {
      let response = await axios.post(`/set_mems`, {
        params: {
          userid: id,
          eventid: this.id,
          confirm: "False",
          typeevent: this.type,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      this.load_info();
      setTimeout(() => {
        this.status = "";
        this.message = "";
        location.reload();
      }, 3000);
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
  },
  mounted() {
    this.load_info();
  },
});
</script>

<template>
  <div class="card-wrapper">
    <div class="card">
      <div class="left">
        <div class="img">
          <Carousel :autoplay="4000" :wrap-around="true">
            <Slide v-for="slide in img" :key="slide">
              <div class="carousel__item">
                <img :src="`/assets/` + slide" alt="" />
              </div>
            </Slide>

            <template #addons>
              <Navigation />
              <Pagination />
            </template>
          </Carousel>
        </div>
        <div class="info">
          <div class="nameWrapp">
            <span class="title">{{ name }}</span>
          </div>
          <div class="place">{{ place }}</div>
          <div class="date">{{ date }}</div>
        </div>
      </div>
      <div class="right">
        <div class="body">
          <span class="description">{{ desc }}</span>
        </div>
      </div>
      <div class="reviews"></div>
      <div class="button-wrapper">
        <button @click="create_req" class="btn publish">
          Отправить запрос на участие
        </button>
      </div>
    </div>
    <div v-if="message" class="notification-container">
      <div :class="{ error: status == 400, success: status == 200 }">
        <span>{{ message }}</span>
      </div>
    </div>
  </div>
  <div class="wrap-reqs" v-if="admin">
    <h1>Запросы на участие</h1>
    <div class="reqs">
      <div class="student" v-for="item in users" :key="item">
        <div class="student-info">
          <img
            @click="this.$router.push({ name: 'profile', query: { id: item } })"
            :src="'/assets/' + item.img.slice(2, -2)"
            alt=""
          />
          <div
            @click="this.$router.push({ name: 'profile', query: { id: item } })"
            class="name"
          >
            {{ item.name + " " + item.surname }}
          </div>
        </div>
        <div class="wrapper-btn">
          <button @click="confirm(item.id)" class="btn publish">
            Подтвердить
          </button>
          <button @click="reject(item.id)" class="btn btn-delete">
            Отлонить
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="wrap-reqs" v-else>
    <h1>Участники</h1>
    <div class="reqs">
      <div
        @click="this.$router.push({ name: 'profile', query: { id: item } })"
        class="student"
        v-for="item in users_mems"
        :key="item"
      >
        <div class="student-info">
          <img src="../assets/no_photo.jpg" alt="" />
          <div class="name">{{ item.name + " " + item.surname }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reqs {
  display: flex;
  gap: 10px;
  flex-direction: column;
}
.student {
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  padding: 10px 15px;
  border-radius: 15px;
  cursor: pointer;

  gap: 15px;
  transition: all 400ms ease;
}

.wrapper-btn {
  display: flex;
  gap: 7px;
  align-items: center;
}

.wrapper-btn button {
  font-size: 0.75rem;
}

.name::after {
  background-color: black; /* Цвет линии при наведении на нее курсора мыши */
  display: block;
  content: "";
  height: 2px; /* Высота линии */
  width: 0%;
  -webkit-transition: width 0.3s ease-in-out;
  -moz--transition: width 0.3s ease-in-out;
  transition: width 0.3s ease-in-out;
}
.name:hover:after,
.name:focus:after {
  width: 100%;
}

.student:hover,
.student:focus {
  transform: translateY(-5px);
}

.student-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.student-info img {
  height: 90px !important;
  width: 90px;
  object-fit: cover;
  border-radius: 100%;
}
.wrap-reqs {
  width: 80%;
  margin: 0 auto;
}

h1 {
  font-size: 2.7rem;
}

::-webkit-scrollbar {
  width: 0;
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

button {
  border-radius: 10px;
  transition: all 500ms;
  font-weight: 550;
}

button:hover {
  transform: scale(1.06);
}

.group {
  width: 90%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.group span {
  font-size: 1.1rem;
  font-weight: 450;
}

.main_info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.main_info .group {
  width: 70%;
}

.main_info .group span {
  color: #000;
}
.modalDelete form {
  display: block;
}

.btn-close {
  border: none;
  position: absolute;
  right: 2%;
  top: 2%;
}

.btn-close:focus,
.btn-close:active,
.btn-close:active:focus:not(:disabled):not(.disabled) {
  box-shadow: none !important;
  outline: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter,
.slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}

input[type="file"] {
  display: none !important;
}
.publish {
  background: linear-gradient(45deg, #56ab2f, #a8e063);
  background-size: 400% 400%;
  animation: gradient 10s ease infinite;
  border-radius: 10px;
  width: auto !important;
  padding: 5px 10px;
  transition: all 400ms;
  color: #fff;
}

.publish:hover {
  transform: scale(1.06);
}
.excel {
  font-weight: 550;
  cursor: pointer;
}
.none {
  display: none;
}
.info {
  overflow-y: scroll !important;
}

.right {
  width: 50%;
}

.nameWrapp {
  display: flex;
  justify-content: space-between;
}
.wrapper .card {
  width: 100%;
  height: 100%;
  min-height: 300px;
}

.left {
  width: 50%;
  height: fit-content;
  display: flex;
  flex-direction: column;
  padding: 20px;
}
.carousel {
  height: 100%;
}
.btn-delete {
  background: linear-gradient(45deg, #ed213a, #93291e);
  background-size: 400% 400%;
  animation: gradient 10s ease infinite;
  border: none;
  border-radius: 10px;
  color: #fff;

  transition: all 500ms ease;
}

@media (max-width: 426px) {
  .wrapper {
    width: 100% !important;
  }
  .card {
    overflow-y: scroll;
    height: 500px;
  }
  .left {
    width: 100%;
  }
  .right {
    width: 100%;
  }

  .img {
    width: 100% !important;
  }
}

.img {
  width: 100%;
  height: auto;
  float: left;
  position: relative;
}

.card-wrapper {
  margin: 0 auto;
  display: flex;
  justify-content: center;
  width: 80%;
  color: var(--mainColor);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  min-height: 400px;
  border-radius: 15px;
}

.wrapper {
  padding: 20px;
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 10px;
  width: 100%;
  overflow-y: scroll;
  height: 400px;
}
.wrapper input {
  padding: 5px;
  border-radius: 10px;
  border: none;
}
.wrapper::-webkit-scrollbar {
  display: none;
}

.wrapper-for-map {
  width: 50%;
  border: 1px solid white;
}

.price {
  font-size: 1.5rem !important;
}

.card {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  padding: 10px;
  background: transparent;
  border: none;
  position: relative;
  width: 100%;
  max-height: 60vh;
  overflow-y: scroll;
  overflow-x: hidden;
}

.carousel__slide {
  width: 100% !important;
}

img {
  width: 100%;
  border-radius: 5px;
  height: 200px !important;
  object-fit: cover;
}

.title {
  font-size: 1.6rem;
}

.place {
  font-size: 1.2rem;
}

.date {
  font-size: 13px;
}

.body {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.button-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 10px;
}

.messengers {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}
.messengers a {
  width: auto;
}

.messengers img {
  height: 27px !important;
  width: auto;
}

.phone {
  font-size: 1.4rem !important;
}

.address {
  font-size: 1rem !important;
}

@media (max-width: 660px) {
  .left,
  .right {
    width: 100%;
  }

  .card-wrapper {
    width: 100%;
  }
}

@media (max-width: 780px) {
  .modalDelete {
    width: 100%;
  }
}
@media (min-width: 661px) and (max-width: 770px) {
  .room {
    flex-direction: column;
  }
}

@media (max-width: 995px) {
  .room {
    padding: 9px 12px;
    width: 90%;
  }

  .left,
  .right {
    width: 100%;
  }

  .button-wrapper {
    margin: 0 auto;
    flex-direction: column;
    flex-basis: 50%;
  }
}

@media (max-width: 380px) {
  .button-wrapper button {
    font-size: small;
  }
}
</style>
