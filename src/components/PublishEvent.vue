<script>
import axios from "axios";
import { defineComponent } from "vue";
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
      img: [],
      files: [],
      counter: 1,
      faculty: [{ counter: 1, depart: [""], name: "" }],
      status: "",
      message: "",
      name: "",
      desc: "",
      date: "",
      place: "",
      types: ["Спорт", "Наука", "Творчество", "Волонтёрство"],
      typeevent: "",
      vuzid: "",
    };
  },
  methods: {
    handleFilesUpload() {
      this.files = this.$refs.files.files;
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
    async publish() {
      let formData = new FormData();
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append("files", file);
      }
      formData.append("vuzid", this.vuzid);
      formData.append("name", this.name);
      formData.append("place", this.place);
      formData.append("date", this.date);
      formData.append("desc", this.desc);
      formData.append("typeevent", this.typeevent);
      let response = await axios.post(`/publish_event`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      setTimeout(() => {
        this.$router.go(-1);
      }, 3000);
    },
    url(file) {
      return URL.createObjectURL(file);
    },
  },
  async mounted() {
    this.vuzid = this.$route.query.id;
  },
});
</script>

<template>
  <div class="wrapper">
    <h1>Публикация мероприятия</h1>
    <form @submit.prevent="submitFiles">
      <div class="wrapper-for-form">
        <div class="col1">
          <div class="img">
            <input
              type="file"
              ref="files"
              id="file"
              multiple
              v-on:change="handleFilesUpload"
            />
            <label v-if="files == `` && img == ``" for="file">
              <div class="line">
                <img src="../assets/img_add.png" alt="" />
              </div>
            </label>

            <Carousel v-if="files != ``" :autoplay="4000" :wrap-around="true">
              <Slide v-for="slide in files" :key="slide">
                <div class="carousel__item">
                  <div class="imgCross">
                    <img :ref="url(slide)" :src="url(slide)" alt="" />
                    <button @click="remove(slide)" class="cross">
                      <ion-icon name="close-outline"></ion-icon>
                    </button>
                  </div>
                </div>
              </Slide>

              <template #addons>
                <Navigation />
                <Pagination />
              </template>
            </Carousel>

            <Carousel v-if="img != ``" :autoplay="4000" :wrap-around="true">
              <Slide v-for="slide in img" :key="slide">
                <div class="carousel__item">
                  <div class="imgCross">
                    <img :src="`/assets/` + slide" alt="" />
                  </div>
                </div>
              </Slide>

              <template #addons>
                <Navigation />
                <Pagination />
              </template>
            </Carousel>
          </div>
        </div>
        <div class="col1">
          <div class="input-group">
            <div class="title">Название:</div>
            <div class="wrapper-for-input">
              <input
                v-model="name"
                type="text"
                name="cityto"
                class="form-input cityto"
                required
                id=""
              />
            </div>
          </div>
          <div class="input-group">
            <div class="title">Место проведения:</div>
            <div class="wrapper-for-input">
              <input
                v-model="place"
                type="text"
                name="cityto"
                class="form-input cityto"
                required
                id=""
              />
            </div>
          </div>
          <div class="input-group">
            <div class="title">Дата:</div>
            <div class="wrapper-for-input">
              <input
                v-model="date"
                type="date"
                name="cityto"
                class="form-input cityto"
                required
                id=""
              />
            </div>
          </div>
          <div class="input-group">
            <div class="title">Описание:</div>
            <div class="wrapper-for-input">
              <textarea
                v-model="desc"
                type="text"
                name="cityto"
                class="form-input cityto"
                required
                id=""
              />
            </div>
          </div>
          <div class="input-group">
            <div class="title">Тип:</div>
            <div class="wrapper-for-input">
              <select
                v-model="typeevent"
                type="text"
                name="cityto"
                class="form-input cityto"
                required
                id=""
              >
                <option :value="item" v-for="item in types" :key="item">
                  {{ item }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
      <div class="div-for-button">
        <button @click="publish" class="publish">Опубликовать</button>
      </div>
    </form>
    <div v-if="message" class="notification-container">
      <div :class="{ error: status == 400, success: status == 200 }">
        <span>{{ message }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-size: 3rem;
  text-align: center;
}
::-webkit-scrollbar {
  display: block;
}

#file {
  display: none;
}
label {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  cursor: pointer;
  border: 1px solid var(--mainColor);
  border-radius: 10px;
  max-height: 200px !important;
  min-height: 200px;
}

.line img {
  width: 50px !important;
  height: 50px !important;
}

.carousel {
  height: 100%;
}
.carousel {
  height: 100%;
}
.carousel__item {
  min-height: 200px;
  width: 100%;
  background-color: var(--vc-clr-primary);
  color: var(--vc-clr-white);
  font-size: 20px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel__slide {
  padding: 10px;
}

.carousel__prev,
.carousel__next {
  box-sizing: content-box;
  border: 5px solid white;
}
.carousel__slide {
  width: 100% !important;
}

.line img {
  width: 50px !important;
  height: 50px !important;
}
.cross {
  color: red;
  z-index: 20;
  background: transparent;
  border: none;
  box-shadow: none;
  height: auto;
  position: absolute;
  top: 4px;
  right: 4px;
  display: flex;
  justify-content: center;
  align-items: center;

  transition: all 500ms;
}

.d-none {
  display: none;
  opacity: 0;

  transition: all 500ms;
}

.active {
  display: block;
  opacity: 1;

  transition: all 500ms;
}

.cross:hover {
  transform: scale(1.4);
}

.imgCross {
  position: relative;
}

@media (max-width: 426px) {
  .img {
    width: 100% !important;
  }
}

.img {
  width: 80%;
  height: auto;
  float: left;
  position: relative;
  min-height: 200px;
  margin: 0 auto;
  border: 2px solid black;
  border-radius: 15px;
}

/* Трансфер */
.wrapper {
  width: 100%;
  display: flex;
  justify-content: start;
  align-items: center;
  flex-direction: column;
  gap: 40px;
  height: 65vh;
  padding: 0;
}

form {
  width: 100%;
  min-height: 70vh;
  overflow-x: hidden;
  overflow-y: scroll;
}
.notification-container {
  margin: 0 auto;
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
.titlebody {
  color: #d5d5d5;
  font-weight: 600;
  position: absolute;
  top: 0%;
  margin-top: 15px;
  font-size: large;
}

.wrapper-for-input {
  flex: 60%;
  width: 50%;
}

.input-group {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.title {
  color: black;
  line-height: 19px !important;
  text-align: start;
  flex: 10%;

  transition: color 300ms;
}

.form-input {
  width: 100%;
}

input,
select {
  border-radius: 5px;
}

.form-input {
  padding: 5px 7px;
  background-color: transparent;
  border: 1px solid #d5d5d5;
  box-shadow: 0px 0 4px 0 black;
  color: black;

  transition: color 300ms;
}

.form-input::placeholder {
  text-align: center;
  font-weight: 500;
  color: black;
}

.form-input:focus,
.form-input:hover {
  color: black;
}

.div-for-button {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.wrapper-for-form {
  width: 100%;
  gap: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: fit-content;
  padding: 8px;
  overflow-y: scroll;
  overflow-x: hidden;
  flex-direction: column;
}

select {
  width: 100%;
  box-sizing: border-box;
  background: transparent;
  color: #fff;
  background-color: transparent !important;
  border: 1px solid #d5d5d5;
  box-shadow: 0px 0 10px 0 #ffffff71;
  padding: 2px;

  transition: all 500ms;
}

.col1 {
  width: 45%;
  display: flex;
  gap: 10px;
  flex-direction: column;
}

.text {
  font-size: 0.9rem !important;
}

.teleg {
  height: 40px !important;
  width: 40px;

  transition: all 400ms;
}

.counter {
  display: flex;
  align-items: center;
  gap: 7px;
}

.counter span {
  font-size: 1.2rem;
}

.counter img {
  height: 25px;
  width: auto;
  cursor: pointer;
}

.group {
  display: flex;
  gap: 20px;
}

.faculty-counter {
  padding: 10px 5px;
  flex-direction: column;
  border: 1px solid #d5d5d5;
  border-radius: 15px;
  box-shadow: 0px 0 4px 0 black;
}

.depart-counter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-left: 10px;
}

.depart-group {
  display: flex;
  gap: 20px;
}

.publish {
  padding: 12px 24px;
  border: 2px solid black;
  border-radius: 8px;

  transition: all 400ms;
}

.publish:hover {
  color: #fff;
  background-color: black;
}

@media screen and (width <=200px) {
  .col1 {
    gap: 5px;
  }

  .title {
    font-size: small;
    width: 20%;
    text-align: end;
    line-height: 0.8;
  }

  .titleMore {
    font-size: 10px;
  }

  .wrapper-for-input {
    margin-left: 10px;
  }

  .input-group {
    gap: 30px;
  }
}

@media (max-width: 420px) {
  .container {
    display: flex;
  }
}

@media (max-width: 570px) {
  .input-group {
    flex-direction: column;
  }
}

@media (max-width: 770px) {
  .wrapper {
    position: relative;
    top: 0;
    flex-direction: column;
  }

  .col1 {
    width: 100%;
  }

  .title {
    line-height: 16px;
  }

  h1 {
    font-size: 2rem;
  }
}

@media (max-width: 800px) {
  .col1 {
    width: 100%;
  }

  .wrapper-for-form {
    flex-direction: column;
  }
}

@media (max-width: 540px) {
  .wrapper-for-form {
    flex-direction: column;
  }
}
</style>
