<script >
import axios from 'axios';
export default {
  name: 'HomeView',
  data() {
    return {
      knnForm: {
        key: '',
        method: ''
      },
      songs: []
    }
  },
  methods: {
    getKnn() {
      const formData = new FormData();
      formData.append('key', this.knnForm.key);
      formData.append('method', this.knnForm.method);
      axios.post('http://127.0.0.1:5000/knn',formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        this.songs = response.data;
        console.log(this.songs);
      }, (error) => {
        console.log(error);
      });
    },
    getPca() {
      const formData = new FormData();
      formData.append('key', this.knnForm.key);
      formData.append('method', this.knnForm.method);
      
      axios.post('http://127.0.0.1:5000/pca',formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        this.songs = response.data;
        console.log(response);
      }, (error) => {
        console.log(error);
      });
    },
    getRtree() {
      const formData = new FormData();
      formData.append('key', this.knnForm.key);
      formData.append('method', this.knnForm.method);
      axios.post('http://127.0.0.1:5000/rtree',formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        this.songs = response.data;
        console.log(response);
      }, (error) => {
        console.log(error);
      });
    },
    async onSubmit() {
      if (this.knnForm.method === 'knn') {
        this.getKnn();
      } else if (this.knnForm.method === 'pca') {
        this.getPca();
      } else if (this.knnForm.method === 'rtree') {
        this.getRtree();
      }
    }
  }
}
</script>

<template>
  <Teleport to="head">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
  </Teleport>
  <main>
    <div class="container mt-3">
      <h2 class="text-center mb-3">Buscador musica</h2>
      <form id="knnForm" @submit.prevent="onSubmit" >
          <div class="d-flex">
            <input type="radio" id="knn" value="knn" v-model="knnForm.method">
            <label for="knn">knn</label><br>
            <input type="radio" id="pca" value="pca" v-model="knnForm.method">
            <label for="pca">pca</label><br>
            <input type="radio" id="rtree" value="rtree" v-model="knnForm.method">
            <label for="rtree">rtree</label>
            <input type="text" class="form-control mb-3 mx-3 w-75" v-model="knnForm.key">
            <button class="btn btn-primary mx-3 w-25 h-75">Enviar</button>
          </div>
      </form>


      <div class="card overflow-auto mx-3">
        <div class="card-body">
          <div v-for="(song, index) in songs" :key="index">
            <!-- Agregar los atributos necesarios -->
            <p>Title: {{ song[1] }}</p>
            <p>Artist: {{ song[2] }}</p>
            <p>Distance: {{ song[3] }}</p>
            <label >------------------------------------</label>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
main {
  min-height: 100vh;
  display: flex;
  align-items: center;
}
</style>