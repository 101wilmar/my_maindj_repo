const addToCartButtons = document.querySelectorAll('.add-cart');

addToCartButtons.forEach(button => {
  button.addEventListener('click', (event) => {
    event.preventDefault();

    const brand = button.dataset.brand;
    const name = button.dataset.name;
    const price = button.dataset.price;
    const imageSrc = button.dataset.image;

    const product = {
      brand: brand,
      name: name,
      price: price,
      imageSrc: imageSrc
    };

    addToCart(product);
  });
});

function addToCart(product) {
  const newItem = document.createElement('div');
  newItem.innerHTML = `
    <img src="${product.imageSrc}" alt="${product.name}">
    <h4>${product.brand}</h4>
    <h5>${product.name}</h5>
    <p>${product.price}</p>
  `;

  const cartItems = document.getElementById('cart-items');
  cartItems.appendChild(newItem);

  const cartTotal = document.getElementById('cart-total');
  const currentTotal = parseInt(cartTotal.innerText);
  cartTotal.innerText = currentTotal + 1;

  fetch('/cart/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(product),
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    });
}
