fetch("http://127.0.0.1:5000/inventory")
  .then(response => response.json())
  .then(events => {
    events.forEach(renderCurrentInventory);
  });

document.querySelector("form").addEventListener("submit", (e) => {
  e.preventDefault();
  const name = document.querySelector("#name").value;
  const brand = document.querySelector("#brand").value;
  const price = document.querySelector("#price").value;
  const stock = document.querySelector("#stock").value;

//   console.log("name",name)
  fetch("http://127.0.0.1:5000/inventory", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({name, brand, price, stock})
  })
  .then(response => response.json())
  .then(renderCurrentInventory);
});

function renderCurrentInventory(item) {
	const li = document.createElement("li");

	const nameh3 = document.createElement("h3");
  	nameh3.textContent = `${item.name}`;
  	
  	const brandSpan = document.createElement("span");
  	brandSpan.textContent = `Brand: ${item.brand}`;
  
  	const priceSpan = document.createElement("span");
  	priceSpan.textContent = `Price: $${item.price}`;

  	const stockSpan = document.createElement("span");
  	stockSpan.textContent = `Stock: ${item.stock}`;
 
	li.appendChild(nameh3);
  	li.appendChild(brandSpan);
  	li.appendChild(document.createElement("br"));
  	li.appendChild(priceSpan);
  	li.appendChild(document.createElement("br"));
  	li.appendChild(stockSpan);
 
  	document.querySelector("#item-list").append(li);
}