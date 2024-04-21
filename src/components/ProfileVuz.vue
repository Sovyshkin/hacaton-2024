<script>
import axios from "axios";
import { Carousel, Navigation, Slide, Pagination } from "vue3-carousel";
export default {
  name: "ProfileVuz",
  components: {
    Carousel,
    Slide,
    Navigation,
    Pagination,
  },
  data() {
    return {
      name: "",
      img: "",
      desc: "",
      id: "",
      edit: false,
      status: "",
      message: "",
      events: [],
    };
  },
  methods: {
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
    async load_info() {
      this.id = this.$route.query.id;
      this.edit = this.$route.query.edit;
      console.log("ID", this.id);
      let response = await axios.post(`/get_vuz`, {
        params: {
          id: this.id,
          namevuz: "False",
          userid: "False",
        },
      });
      this.name = response.data.namevuz;
      if (response.data.photoprof) {
        this.img = JSON.parse(response.data.photoprof.replace(/'/g, '"'));
      } else {
        this.img = "no_photo.jpeg";
      }
      this.adress = response.data.geovuz;
      this.desc = response.data.taskprof;
      let response2 = await axios.post(`/get_events`, {
        params: {
          vuzid: this.id,
        },
      });
      console.log(response2.data.events);
      if (response2.data.events) {
        this.events = JSON.parse(response2.data.events.replace(/'/g, '"'));
        console.log(this.events);
      }
    },
    async save() {
      let response = await axios.post("/save_desc", {
        params: {
          id: this.id,
          desc: this.desc,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      setTimeout(() => {
        this.status = "";
        this.message = "";
      }, 3000);
    },

    open(id) {
      this.$router.push({
        name: "event",
        query: { id },
      });
    },
  },
  mounted() {
    this.load_info();
  },
};
</script>
<template>
  <div class="wrapper-for-profile">
    <div class="header-info">
      <div class="img">
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
      <div class="info">
        <div class="name">{{ name }}</div>
        <div class="vuz">
          {{ adress }}
        </div>
      </div>
    </div>
    <div v-if="!edit" class="desc">
      {{ desc }}
    </div>
    <textarea
      v-if="edit"
      class="desc-text"
      v-model="desc"
      id=""
      cols="30"
      rows="10"
      placeholder="Расскажите о ВУЗе..."
      @blur="save"
    ></textarea>
    <h1>Мероприятия</h1>
    <div class="news">
      <div
        class="add-news"
        @click="
          this.$router.push({ name: 'publishevent', query: { id: this.id } })
        "
      >
        <img src="../assets/add_news.png" alt="" />
      </div>
      <div class="card" v-for="(item, i) in events" :key="item">
        <img
          class="news-img"
          @click="open(item.id)"
          :src="'/assets/' + item.photoprof[0]"
          alt=""
        />
        <div class="card-body">
          <h5 class="card-title">
            <span class="title">{{ item.name }}</span>
          </h5>
          <div class="accordion" id="accordionExample">
            <div class="accordion-item">
              <h2 class="accordion-header" :id="`heading${i}`">
                <button
                  class="accordion-button collapsed"
                  type="button"
                  data-bs-toggle="collapse"
                  :data-bs-target="`#collapse${i}`"
                  aria-expanded="false"
                  :aria-controls="`collapse${i}`"
                >
                  Подробнее
                </button>
              </h2>
              <div
                :id="`collapse${i}`"
                class="accordion-collapse collapse"
                :aria-labelledby="`heading${i}`"
                data-bs-parent="#accordionExample"
              >
                <div class="accordion-body">
                  {{ item.taskprof }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="message" class="notification-container">
      <div :class="{ error: status == 400, success: status == 200 }">
        <span>{{ message }}</span>
      </div>
    </div>
  </div>
</template>
<style scoped>
.img {
  width: 40%;
  height: auto;
  float: left;
  position: relative;
  min-height: 200px;
  margin: 0 auto;
  border-radius: 15px;
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
.notification-container {
  position: absolute;
  top: -5%;
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
textarea {
  max-height: 100px;
}

.d-none {
  display: flex;
}

.edit-vuz {
  border-radius: 10px;
  font-size: 0.65rem;
  padding: 2px 4px;
}

.vuz,
.faculty,
.depart {
  display: flex;
  align-items: center;
  gap: 7px;
}

.vuz select,
.faculty select,
.depart select {
  min-width: 60px;
  border: 1px solid black;
  border-radius: 5px;
}

h1 {
  font-size: 3rem;
}
.accordion-body {
  background-color: #f7ede8;
}
.add-news {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 290px;
  max-height: 290px;
  min-width: 290px;
  max-width: 290px;
  border: 2px dashed black;
  border-radius: 15px;
}
.accordion-body button {
  display: block;
  margin: 0 auto;
  border: none;
  width: 100%;
  padding: 5px 0;
  box-shadow: 0 0 10px 0 #00000037;
}

.accordion-button {
  background-color: #f7ede8 !important;
  background: transparent;
  outline: none !important;
  border: none !important;
  box-shadow: none !important;
  color: black !important;
}
.news-img {
  width: auto;
  max-height: 180px;
  min-height: 180px;
  object-fit: cover;
  border-radius: 15px 15px 0 0;
}
.price {
  font-size: 13px;
}
h5 {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card {
  flex: 30%;
  color: var(--mainColor);
  background-color: transparent;
  cursor: pointer;
  min-height: 290px;
  max-width: 320px;
  box-shadow: 0 0 10px 0 black;
  border-radius: 15px;
  position: relative;

  transition: all 400ms;
}
.card:hover {
  box-shadow: 0 0 10px 0 var(--mainColor);
  transform: scale(105%);
}
.news {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.add-news {
  flex: 30%;
  padding: 15px;
  cursor: pointer;
}

.add-news img {
  height: 70px;
}
#file {
  display: none;
}

.ava {
  border-radius: 15px;
}

.desc-text {
  width: 100%;
  padding: 10px 20px;
  background-color: #ddd5d0;
  border-radius: 15px;
  outline: none;
}

.image {
  padding: 10px;
  border-radius: 15px;
  border: 1px solid black;
}
.wrapper-for-profile {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
}

.add_img {
  height: 60px !important;
  cursor: pointer;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-info img {
  height: 200px;
}

.info {
  width: 60%;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.name,
.surname {
  font-size: 3rem;
}

.rating {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.rating img {
  height: 30px;
}

.desc {
  padding: 10px 20px;
  background-color: #ddd5d0;
  border-radius: 15px;
}

@media (max-width: 850px) {
  .name,
  .surname {
    font-size: 2rem;
  }

  .ava {
    height: 120px !important;
  }
}

@media (max-width: 550px) {
  .header-info {
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .ava {
    height: 150px !important;
  }
}
</style>
