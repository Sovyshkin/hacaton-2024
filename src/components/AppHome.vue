<script>
import axios from "axios";

export default {
  name: "App",
  components: {},
  data() {
    return {
      topstudents: [],
    };
  },
  methods: {
    async load_info() {
      let response = await axios.post(`/get_top`);
      console.log(response.data.topusers);
      if (response.data.topusers) {
        this.topstudents = JSON.parse(
          response.data.topusers.replace(/'/g, '"')
        );
      }
    },
  },
  mounted() {
    this.load_info();
  },
};
</script>
<template>
  <div class="wrap-home">
    <div class="title">
      <div class="desc">
        <span class="desc-title"
          >LifeCource — это ваш личный помощник в мире образования</span
        >
        <div class="list-desc">
          <div class="group-desc">
            <img src="../assets/students.png" alt="" />
            <span>Сообщество студентов</span>
          </div>
          <div class="group-desc">
            <img src="../assets/news.png" alt="" />
            <span>Лента новостей</span>
          </div>
          <div class="group-desc">
            <img src="../assets/medal.png" alt="" />
            <span>Система достижений</span>
          </div>
        </div>
      </div>
      <img class="title-img" src="../assets/vuz.jpeg" alt="" />
    </div>
    <div class="top-students">
      <span class="desc-title">ТОП студентов:</span>
      <div class="list-students">
        <div
          class="student"
          @click="
            this.$router.push({ name: 'profile', query: { id: item.id } })
          "
          v-for="item in topstudents"
          :key="item"
        >
          <div class="left">
            <img
              src="../assets/no_photo.jpg"
              class="ava"
              :class="{ 'd-none': !item.photoprof.includes('no_photo') }"
              alt=""
            />
            <img
              :src="'/assets/' + item.photoprof"
              :class="{ 'd-none': item.photoprof.includes('no_photo') }"
              alt=""
              class="ava"
            />
            <div class="student-info">
              <span>{{ item.name + " " + item.surname }}</span>
              <span>{{ item.vuzuser }}</span>
            </div>
          </div>
          <div class="right">
            <span>{{ item.zvezd }}</span>
            <img src="../assets/star.png" class="star-ico" alt="" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.right {
  display: flex;
  align-items: center;
  gap: 7px;
}
.student-info {
  display: flex;
  flex-direction: column;
}
.wrap-home {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.title {
  display: flex;
  gap: 20px;
}

.desc {
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.list-desc {
  display: flex;
  gap: 20px;
}

.group-desc {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;

  transition: all 400ms ease;
}

.group-desc:hover {
  transform: translateY(-5px);
}

.group-desc span {
  text-align: center;
}

.desc-title {
  font-size: 3rem;
}

.title-img {
  width: 60%;
  max-height: 55vh;
  object-fit: cover;
  border-radius: 15px;
}

.group-desc img {
  width: 80px;
}

.list-students {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.star-ico {
  height: 30px !important;
}

.student {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  border-radius: 15px;
  cursor: pointer;

  transition: all 400ms ease;
}

.student:hover,
.student:focus,
.student:active {
  transform: translateY(-5px);
}

.ava {
  height: 90px;
  width: 90px;
  border-radius: 100%;
}

.top-students {
  display: flex;
  gap: 10px;
  flex-direction: column;
}

@media (max-width: 1000px) {
  .title {
    flex-direction: column;
  }

  .title-img {
    width: 100% !important;
    height: 40vh !important;
  }

  .list-desc {
    justify-content: center;
  }
}
</style>
