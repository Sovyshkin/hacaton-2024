<script>
import Header from "@/components/Header.vue";
export default {
  name: "App",
  components: {
    Header,
  },
};
</script>
<template>
  <div class="wrapper">
    <Header />
    <router-view></router-view>
  </div>
</template>
<style>
@import url("https://fonts.googleapis.com/css2?family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
* {
  padding: 0px;
  margin: 0px;
  border: none;
  font-family: "Montserrat Alternates", sans-serif;
  font-weight: 400;
  font-style: normal;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

/* Links */

a,
a:link,
a:visited {
  text-decoration: none;
}

a:hover {
  text-decoration: none;
}

/* Common */

aside,
nav,
footer,
header,
section,
main {
  display: block;
}

h1,
h2,
h3,
h4,
h5,
h6,
p {
  font-size: inherit;
  font-weight: inherit;
}

ul,
ul li {
  list-style: none;
}

img {
  vertical-align: top;
}

img,
svg {
  max-width: 100%;
  height: auto;
}

address {
  font-style: normal;
}

/* Form */

input,
textarea,
button,
select {
  font-family: inherit;
  font-size: inherit;
  color: inherit;
  background-color: transparent;
}

input::-ms-clear {
  display: none;
}

button,
input[type="submit"] {
  display: inline-block;
  box-shadow: none;
  background-color: transparent;
  background: none;
  cursor: pointer;
}

input:focus,
input:active,
button:focus,
button:active {
  outline: none;
}

button::-moz-focus-inner {
  padding: 0;
  border: 0;
}

label {
  cursor: pointer;
}

legend {
  display: block;
}
.wrapper {
  width: 100%;
  min-height: 100vh;
  padding: 50px 150px;
  background-color: #f7ede8;
  display: flex;
  flex-direction: column;
  gap: 70px;
}

@media (max-width: 1260px) {
  .wrapper {
    padding: 25px 75px;
  }
}

@media (max-width: 730px) {
  .wrapper {
    padding: 20px 40px;
  }

  .logo {
    margin-right: 0;
  }

  .btn {
    padding: 8px 12px;
  }
}

@media (max-width: 400px) {
  .wrapper {
    padding: 12px 25px;
  }
}

@media (max-width: 315px) {
  .wrapper {
    padding: 10px 5px;
  }
}
</style>
