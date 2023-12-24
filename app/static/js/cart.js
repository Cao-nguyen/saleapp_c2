function addToCart(id, name, price, image){
    fetch("http://127.0.0.1:5000/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name":name,
            "price":price,
            "image": image
        }),
        headers:{
            'Content-Type': "application/json"
        }
    })
    .then(function(res){
        return res.json()
    })
    .then(function(result){
        let cartCount = document.getElementById("cart-number")
        cartCount.innerText = result.total_quantity
    });
}

function removeItem(id){
    fetch(`/api/cart/${id}`, {
        method: 'delete'
    })
    .then(res => {
        return res.json()
    })
    .then(result => {
        let cartCount = document.getElementById("cart-number")
        let cartTotalPrice = document.getElementById("cart-total")
        cartCount.innerText = result.total_quantity
        cartTotalPrice.innerText = result.total_price
        hideItem(id)
    })
}

function hideItem(product_id){
    productItem = document.getElementById(`product${product_id}`)
    productItem.style.display = "None"
}

function updateItem(id, price, object){
    fetch(`/api/cart/${id}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": object.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        return res.json()
    })
    .then(result => {
        let cartCount = document.getElementById("cart-number")
        let cartTotalPrice = document.getElementById("cart-total")
        let productPrice = document.getElementById(`product-price${id}`)
        cartCount.innerText = result["count_cart"]["total_quantity"]
        cartTotalPrice.innerText = result["count_cart"]["total_price"]
        productPrice.innerText = price * result["quantity_update"]
    })
}