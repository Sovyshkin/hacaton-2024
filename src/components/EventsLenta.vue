<script>
import axios from "axios";

export default {
  name: "AppLenta",
  components: {},
  data() {
    return {
      news: [],
    };
  },
  methods: {
    async load_info() {
      let response = await axios.post(`/lenta_events`);
      if (response.data.publication) {
        this.news = JSON.parse(response.data.publication.replace(/'/g, '"'));
      }
    },
    open(id) {
      this.$router.push({ name: "event", query: { id } });
    },
  },
  mounted() {
    this.load_info();
  },
};
</script>
<template>
  <h1>Мероприятия</h1>
  <div class="news">
    <div class="card" v-for="(item, i) in news" :key="item">
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
</template>
<style scoped>
.btn-danger {
  margin: 0 auto;
  max-width: 100px;
  border-radius: 10px;
}
.achievments {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 20px;
}

.achiev {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.achiev img {
  height: 120px;
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
  min-width: 290px;
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

@media (max-width: 660px) {
  .card {
    margin: 0 auto;
    flex: 100%;
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
