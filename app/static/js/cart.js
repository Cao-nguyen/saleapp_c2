function addToCart(id, name, price){
    fetch("http://127.0.0.1:5000/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name":name,
            "price":price
        }),
        headers:{
            'Content-Type': "application/json"
        }
    })
    .then(function(res){
        return res.json()
    })
    .then(function(result){
        let cartCount = document.getElementById("cart-count")
        cartCount.innerText = result.total_quantity
    });
}