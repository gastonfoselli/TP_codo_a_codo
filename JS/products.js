const { createApp } = Vue;
createApp({
  data() {
    return {
      productos: [],
      url: 'http://localhost:5500/productos', 
      error: false,
      cargando: true,
      
      ProductID: 0,
      ProductName: "",
      CategoryID: 0,
      ManufacturerID: 0,
      Price: 0,
      StockQuantity: 0,
      Description: "",
      Image: "",
    };
  },
  
  methods: {
    fetchData(url) {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          this.productos = data;
          this.cargando = false;
        })
        .catch(err => {
          console.error(err);
          this.error = true;
        });
    },
    eliminar_producto(ProductID) {
      const url = this.url + ProductID;
      var options = {
        method: 'DELETE',
      };
      fetch(url, options)
        .then(res => res.json())
        .then(res => {
          alert('Registro Eliminado');
          location.reload();
        });
    },
    agregar_producto() {
      let producto = {
        ProductName: this.ProductName,
        CategoryID: this.CategoryID,
        ManufacturerID: this.ManufacturerID,
        Price: this.Price,
        StockQuantity: this.StockQuantity,
        Description: this.Description,
        Image: this.Image
      };
      var options = {
        body: JSON.stringify(producto),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow'
      };
      fetch(this.url, options)
        .then(function () {
          alert("Registro guardado");
          window.location.href = "index.html";
        })
        .catch(err => {
          console.error(err);
          alert("Error al Guardar");
        });
    }
  },
  created() {
    this.fetchData(this.url);
  }
}).mount('#app');