<script>
import axios from "axios";
import { defineComponent } from "vue";

export default defineComponent({
  components: {},
  data() {
    return {
      id: "",
      img: "",
      desc: "",
      message: "",
      status: "",
      comments: [],
      likes: 0,
      userid: "",
      name: "",
      surname: "",
      hash: "",
      user: {},
      likef: false,
      textComment: "",
    };
  },
  methods: {
    async load_info() {
      this.id = this.$route.query.id;
      let response = await axios.post(`/get_entry`, {
        params: {
          id: this.id,
        },
      });

      this.img = response.data.img;
      this.desc = response.data.desc;
      this.hash = response.data.hash;
      console.log(response.data.comments.replace(/'/g, '"'));
      if (response.data.comments) {
        this.comments = JSON.parse(response.data.comments.replace(/'/g, '"'));
      }
      this.likes = response.data.likes;
      this.userid = response.data.userid;
      let response2 = await axios.post(`/info-profile`, {
        params: {
          id: this.userid,
        },
      });
      this.name = response2.data.nameprof;
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

    async like() {
      this.likef = true;
      let response = await axios.post(`/set_like`, {
        params: {
          id: this.id,
        },
      });
      let status = response.data.status;
      if (status == 200) {
        this.load_info();
      }
    },

    async setComment() {
      let id = this.getCookieValue("id");
      let res = await axios.post(`/info-profile`, {
        params: {
          id: id,
        },
      });
      let name = res.data.nameprof;
      let surname = res.data.surnameprof;
      let img = res.data.photoprof;
      let response = await axios.post(`/set_koment`, {
        params: {
          id: this.id,
          text: this.textComment,
          name: name,
          surname: surname,
          img: img,
          userid: id,
        },
      });
      let status = response.data.status;
      if (status == 200) {
        this.load_info();
        this.textComment = "";
      }
    },

    async getUser(id) {
      let response = await axios.post(`/info-profile`, {
        params: {
          id: id,
        },
      });
      let user = { name: "", surname: "", img: "" };
      user.name = response.data.nameprof;
      user.surname = response.data.surnameprof;
      user.img = response.data.photoprof;
      return user;
    },
  },
  mounted() {
    this.load_info();
  },
});
</script>

<template>
  <h1>Запись</h1>
  <div class="card-wrapper">
    <div class="card">
      <div class="left">
        <div class="img">
          <img :src="'/assets/' + img" alt="" />
        </div>
        <div class="info">
          <div class="date">{{ hash }}</div>
        </div>
      </div>
      <div class="right">
        <div class="body">
          <span class="description">{{ desc }}</span>
        </div>
      </div>
      <div class="reviews"></div>
    </div>
    <div @click="like" v-if="!likef" class="group-likes">
      <span>{{ likes }}</span>
      <img src="../assets/like.png" alt="" />
    </div>
    <div v-if="likef" class="group-likes likef">
      <span>{{ likes }}</span>
      <img src="../assets/like.png" alt="" />
    </div>
    <div v-if="message" class="notification-container">
      <div :class="{ error: status == 400, success: status == 200 }">
        <span>{{ message }}</span>
      </div>
    </div>
  </div>
  <div class="wrap-comment">
    <h3>Оставьте комментарий</h3>
    <div class="comment">
      <textarea
        v-model="textComment"
        cols="30"
        rows="10"
        placeholder="Введите сообщение..."
      ></textarea>
      <img @click="setComment" src="../assets/send.png" alt="" />
    </div>
  </div>
  <div class="wrap-reqs">
    <h1>Комментарии</h1>
    <div class="reqs">
      <div class="student" v-for="item in comments" :key="item">
        <div class="student-info">
          <img
            @click="
              this.$router.push({ name: 'profile', query: { id: item.userid } })
            "
            :src="'/assets/' + item.img"
            alt=""
          />
          <div
            @click="
              this.$router.push({ name: 'profile', query: { id: item.userid } })
            "
            class="name"
          >
            <span class="name2">{{ item.name + " " + item.surname }}</span>
            <span>{{ item.text }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h3 {
  font-size: 2rem;
}
.wrap-comment {
  width: 80%;
  display: flex;
  flex-direction: column;
  max-height: 100px;
  margin: 0 auto;
}

.comment {
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment img {
  height: 30px !important;
  width: auto !important;
  cursor: pointer;

  transition: all 400ms ease;
}

.comment img:hover {
  transform: translateY(-5px);
}

.comment textarea {
  border: 1px solid black;
  border-radius: 15px;
  padding: 10px 20px;
  max-height: 100px;
  width: 50%;
}
.likef {
  background-color: black !important;
  color: #fff !important;
}
.group-likes {
  cursor: pointer;
  padding: 7px;
  border: 1px solid black;
  border-radius: 10px;
  position: absolute;
  left: 5%;
  bottom: 5%;
  display: flex;
  align-items: center;
  gap: 10px;

  transition: all 400ms ease;
}

.group-likes:hover,
.group-likes:active {
  background-color: black;
  color: #fff;
}

.group-likes img {
  height: 30px !important;
  width: auto !important;
}

h1 {
  text-align: center;
  font-size: 3rem;
}
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

.name2::after {
  background-color: black; /* Цвет линии при наведении на нее курсора мыши */
  display: block;
  content: "";
  height: 2px; /* Высота линии */
  width: 0%;
  -webkit-transition: width 0.3s ease-in-out;
  -moz--transition: width 0.3s ease-in-out;
  transition: width 0.3s ease-in-out;
}
.name2:hover:after,
.name2:focus:after {
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

.name {
  display: flex;
  flex-direction: column;
}

.nameWrapp {
  display: flex;
  justify-content: space-between;
  gap: 10px;
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
  position: relative;
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
  max-width: 410px;
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
  margin-top: 10px;
  font-size: 13px;
}

.body {
  margin-top: 10px;
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
