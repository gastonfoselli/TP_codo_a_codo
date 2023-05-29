<<<<<<< HEAD
$('.like-btn').on('click', function() {
    $(this).toggleClass('is-active');
 });

 $('.minus-btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
 
    if (value > 1)  {
        value = value - 1;
    } else {
        value = 0;
    }
 
  $input.val(value);
 
});
 
function substract_quantity (param) {
    let x=document.getElementById(param);
    let value_new = parseInt(x.value);
 
    if (value_new >= 1) {
        value_new = value_new - 1;
    } else {
        value_new =0;
    }
 
    x.value=value_new;
}

function add_quantity (param) {
    let x=document.getElementById(param);
    let value_new = parseInt(x.value);
 
    if (value_new < 100) {
        value_new = value_new + 1;
    } else {
        value_new =100;
    }
 
    x.value=value_new;
}

function total_price (param, param2) {
    let x=document.getElementById(param);
    let total_new = parseInt(x.name);
    let y=document.getElementById(param2);
    let quantity=parseInt(y.value);

    x.value="$ "+total_new*quantity;
}

function delete_item (e) {
    e.parentElement.remove();
}

function hide_show () {
    let x = document.getElementById("cart")
    if(x.style.display==="flex") {
        x.style.display="none"
    } else {x.style.display="flex"}
}

function cart_position () {
    let x = document.getElementById("cart");
    let y = document.getElementById("carrito_grande");
    let z = document.getElementById("carrito_chico");
    if(window.innerWidth>2400) {
        y.appendChild(x)
    } else {
        z.appendChild(x)
    }
}
function new_nav_bar (){
    let x = document.getElementById("small_size_cart");
    let y = document.getElementById("big_size_cart");
    if(window.innerWidth>500) {
        x.style.display = "none";
        y.style.display = "flex";
    } else {
        y.style.display = "none";
        x.style.display = "flex";
    }
}


const create_Li = (cliente) => {
    const Picture = document.createElement("img");
    Picture.src = `${cliente.picture.large}`;
    return Picture
    };

    const create_LiNombre = (cliente) => {
        const Picture = document.createElement("p");
        Picture.textContent = `${cliente.name.first} ${cliente.name.last}`;
        return Picture
        };
    
    const appendToDOM = (users) => {
    const ul = document.querySelector(".clienteImagen");
    users.map((cliente) => {
    ul.appendChild(create_Li(cliente));
      });
    };
    
    const appendToDOMName = (users) => {
        const ul = document.querySelector(".clienteNombre");
        users.map((cliente) => {
        ul.appendChild(create_LiNombre(cliente));
          });
        };
    
    function fetch_Users () {
    axios
        .get("https://randomuser.me/api/")
        .then((response) => {
    const users = response.data.results/* .data */;
    appendToDOM(users);
    appendToDOMName(users);
        })
        .catch((error) =>console.error(error));
    };
=======
$('.like-btn').on('click', function() {
    $(this).toggleClass('is-active');
 });

 $('.minus-btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
 
    if (value > 1)  {
        value = value - 1;
    } else {
        value = 0;
    }
 
  $input.val(value);
 
});
 
function substract_quantity (param) {
    let x=document.getElementById(param);
    let value_new = parseInt(x.value);
 
    if (value_new >= 1) {
        value_new = value_new - 1;
    } else {
        value_new =0;
    }
 
    x.value=value_new;
}

function add_quantity (param) {
    let x=document.getElementById(param);
    let value_new = parseInt(x.value);
 
    if (value_new < 100) {
        value_new = value_new + 1;
    } else {
        value_new =100;
    }
 
    x.value=value_new;
}

function total_price (param, param2) {
    let x=document.getElementById(param);
    let total_new = parseInt(x.name);
    let y=document.getElementById(param2);
    let quantity=parseInt(y.value);

    x.value="$ "+total_new*quantity;
}

function delete_item (e) {
    e.parentElement.remove();
}

function hide_show () {
    let x = document.getElementById("cart")
    if(x.style.display==="flex") {
        x.style.display="none"
    } else {x.style.display="flex"}
}

function cart_position () {
    let x = document.getElementById("cart");
    let y = document.getElementById("carrito_grande");
    let z = document.getElementById("carrito_chico");
    if(window.innerWidth>2400) {
        y.appendChild(x)
    } else {
        z.appendChild(x)
    }
}
function new_nav_bar (){
    let x = document.getElementById("small_size_cart");
    let y = document.getElementById("big_size_cart");
    if(window.innerWidth>500) {
        x.style.display = "none";
        y.style.display = "flex";
    } else {
        y.style.display = "none";
        x.style.display = "flex";
    }
}
>>>>>>> 67025049da78affd56284a5827c2bd9cce6281d5
