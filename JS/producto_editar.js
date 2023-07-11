console.log(location.search);
const urlParams = new URLSearchParams(window.location.search);
const ProductID = urlParams.get('id');
console.log(ProductID);

const { createApp } = Vue;
createApp({
  data() {
    return {
      ProductID: 0,
      ProductName: "",
      CategoryID: 0,
      ManufacturerID: 0,
      Price: 0,
      StockQuantity: 0,
      Description: "",
      Image: "",
      url: 'http://localhost:5500/productos/' + ProductID,
      mostrarFormulario: false
    };
  },
  methods: {
    fetchData(url) {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.ProductID = data.ProductID;
          this.ProductName = data.ProductName;
          this.CategoryID = data.CategoryID;
          this.ManufacturerID = data.ManufacturerID;
          this.Price = data.Price;
          this.StockQuantity = data.StockQuantity;
          this.Description = data.Description;
          this.Image = data.Image;
        })
        .catch(err => {
          console.error(err);
          this.error = true;
        });
    },
    modificar_producto() {
      let product = {
        ProductName: this.ProductName,
        CategoryID: this.CategoryID,
        ManufacturerID: this.ManufacturerID,
        Price: this.Price,
        StockQuantity: this.StockQuantity,
        Description: this.Description,
        Image: this.Image
      };
      var options = {
        body: JSON.stringify(product),
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow'
      };
      fetch(this.url, options)
        .then(function () {
          alert("Registro modificado");
          window.location.href = "index.html";
        })
        .catch(err => {
          console.error(err);
          alert("Error al Modificar");
        });
    },
    irAFormulario() {
      this.mostrarFormulario = true;
    }
  },
  created() {
    this.fetchData(this.url);
  }
}).mount('#app');
