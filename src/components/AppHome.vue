<script>
export default {
  name: "App",
  components: {},
  data() {},
  methods: {},
  mounted() {},
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
        <div class="student">
          <img src="../assets/no_photo.jpg" alt="" />
          <div class="student-info">Имя Фамилия</div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
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
}

.student {
  display: flex;
  align-items: center;
  gap: 15px;
}

.student img {
  height: 90px;
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
