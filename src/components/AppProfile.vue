<script>
import axios from "axios";
export default {
  name: "AppProfile",
  components: {},
  data() {
    return {
      name: "",
      surname: "",
      img: "",
      rating: "20",
      faculty: "факультет",
      depart: "кафедра",
      desc: "",
      id: "",
      edit: false,
      vuz: "",
      news: [
        {
          img: "2024-04-20_13-44-32-119452.jpeg",
          title: "Первая запись",
          desc: "Описание",
        },
        {
          img: "2024-04-20_13-44-32-119452.jpeg",
          title: "Первая запись",
          desc: "Описание",
        },
        {
          img: "2024-04-20_13-44-32-119452.jpeg",
          title: "Первая запись",
          desc: "Описание",
        },
      ],
      vuzs: [],
      status: "",
      message: "",
      userfak: "",
      userkaf: "",
      objfak: { depart: [] },
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
      if (this.$route.query.id) {
        this.id = this.$route.query.id;
        this.edit = false;
      } else {
        this.id = this.getCookieValue("id");
        this.edit = true;
      }
      let response = await axios.post(`/info-profile`, {
        params: {
          id: this.id,
        },
      });
      this.name = response.data.nameprof;
      this.surname = response.data.surnameprof;
      this.img = response.data.photoprof.slice(2, -2);
      this.desc = response.data.desc;
      if (response.data.vuzuser == "None") {
        this.vuz = "";
      } else {
        this.vuz = response.data.vuzuser;
      }
      this.userkaf = response.data.kaf;

      let data = await axios.post(`/get_vuzs`);
      console.log(data.data.vuzs);
      if (data.data.vuzs) {
        this.vuzs = JSON.parse(data.data.vuzs.replace(/'/g, '"'));
      }
      if (this.vuz) {
        let response = await axios.post(`/get_vuz`, {
          params: {
            namevuz: this.vuz,
          },
        });
        if (response.data.fakultet) {
          this.faculty = JSON.parse(response.data.fakultet.replace(/'/g, '"'));
          if (this.faculty) {
            this.faculty.forEach((obj) => {
              if (obj.name == response.data.fak) {
                this.objfak = obj;
              }
            });
          }
        }
      }
    },
    async handleFilesUpload() {
      this.files = this.$refs.files.files;
      let formData = new FormData();
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append("files", file);
      }
      formData.append("id", this.id);
      let response = await axios.post(`/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      setTimeout(() => {
        location.reload();
        this.status = "";
        this.message = "";
      }, 3000);
    },
    async publish() {
      let formData = new FormData();
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append("files", file);
      }
      let response2 = await axios.post(`/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      let id = response2.data.id;
      let response = await axios.post(`/registration-vuz`, {
        params: {
          id: id,
          nameprof: this.name,
          geovuz: this.adress,
          fakprof: this.faculty,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      setTimeout(() => {
        this.$router.push({ name: "profile" });
      }, 3000);
    },
    url(file) {
      return URL.createObjectURL(file);
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
        location.reload();
        this.status = "";
        this.message = "";
      }, 3000);
    },

    async save_vuz() {
      let response = await axios.post(`/set_vuz`, {
        params: {
          id: this.getCookieValue("id"),
          vuz: this.vuz,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      setTimeout(() => {
        this.status = "";
        this.message = "";
      }, 3000);
    },

    async save_fak() {
      let response = await axios.post(`/set_fak`, {
        params: {
          id: this.getCookieValue("id"),
          fak: this.userfak,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      this.load_info();
      setTimeout(() => {
        this.status = "";
        this.message = "";
      }, 3000);
    },

    async save_kaf() {
      let response = await axios.post(`/set_kaf`, {
        params: {
          id: this.getCookieValue("id"),
          kaf: this.userkaf,
        },
      });
      this.status = response.data.status;
      this.message = response.data.message;
      this.load_info();
      setTimeout(() => {
        this.status = "";
        this.message = "";
      }, 3000);
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
      <div class="image" v-if="img.includes('no_photo')">
        <input
          type="file"
          ref="files"
          id="file"
          v-on:change="handleFilesUpload"
        />
        <label for="file">
          <img src="../assets/img_add.png" class="add_img" alt="" />
        </label>
      </div>
      <img v-else class="ava" :src="`/assets/${img}`" alt="" />
      <div class="info">
        <div class="name">{{ name }}</div>
        <div class="surname">{{ surname }}</div>
        <div class="vuz">
          <label v-if="!vuz" for="vuz">ВУЗ не выбран</label>
          <label v-if="vuz" for="vuz">ВУЗ:</label>
          <select v-if="!vuz" v-model="vuz" id="vuz" @blur="save_vuz">
            <option v-for="(item, i) in vuzs" :value="item" :key="i">
              {{ item }}
            </option>
          </select>
          <span v-if="vuz">{{ vuz }}</span>
          <button
            v-if="vuz"
            @click="this.vuz = ''"
            class="btn btn-info edit-vuz"
          >
            Изменить
          </button>
        </div>
        <div class="faculty">
          <label v-if="!userfak" for="vuz">Факультет не выбран</label>
          <label v-if="userfak" for="vuz">Факультет:</label>
          <select v-if="!userfak" v-model="userfak" id="fak" @blur="save_fak">
            <option v-for="(item, i) in faculty" :value="item.name" :key="i">
              {{ item.name }}
            </option>
          </select>
          <span v-if="userfak">{{ userfak }}</span>
          <button
            v-if="userfak"
            @click="this.userfak = ''"
            class="btn btn-info edit-vuz"
          >
            Изменить
          </button>
        </div>
        <div class="depart" v-if="objfak">
          <label v-if="!userkaf" for="vuz">Кафедра не выбрана</label>
          <label v-if="userkaf" for="vuz">Кафедра:</label>
          <select v-if="!userkaf" v-model="userkaf" id="kaf" @blur="save_kaf">
            <option v-for="(item, i) in objfak.depart" :value="item" :key="i">
              {{ item }}
            </option>
          </select>
          <span v-if="userkaf">{{ userkaf }}</span>
          <button
            v-if="userkaf"
            @click="this.userkaf = ''"
            class="btn btn-info edit-vuz"
          >
            Изменить
          </button>
        </div>
      </div>
      <div class="rating">
        <img src="../assets/star.png" alt="" />
        <span>{{ rating }}</span>
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
      placeholder="О себе..."
    ></textarea>
    <h1>Записи</h1>
    <div class="news">
      <div class="add-news" @click="this.$router.push({ name: 'publishnews' })">
        <img src="../assets/add_news.png" alt="" />
      </div>
      <div class="card" v-for="(item, i) in news" :key="item">
        <img
          class="news-img"
          @click="open"
          :src="'/assets/' + item.img"
          alt=""
        />
        <div class="card-body">
          <h5 class="card-title">
            <span class="title">{{ item.title }}</span>
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
                  {{ item.desc }}
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

.vuz select {
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
