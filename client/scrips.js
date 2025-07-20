fetch("http://127.0.0.1:5000/inventory")
  .then(response => response.json())
  .then(events => {
    events.forEach(renderCurrentInventory);
  });

//POST:List Inventory Details  
document.querySelector("#add-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const name = document.querySelector("#name").value;
  const barcode = document.querySelector("#barcode").value;
  const price = document.querySelector("#price").value;
  const stock = document.querySelector("#stock").value;

  fetch("http://127.0.0.1:5000/inventory", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({name, barcode, price, stock})
  })
  .then(response => response.json())
  .then(renderCurrentInventory); 
  document.querySelector("#add-form").reset(); 
});

function renderCurrentInventory(item) {
	const li = document.createElement("li");
	const nameh3 = document.createElement("h3");
  	nameh3.textContent = `${item.name}`;
	const barcodeSpan = document.createElement("span");
  	barcodeSpan.textContent = `Barcode: ${item.barcode}`;
  	const priceSpan = document.createElement("span");
  	priceSpan.textContent = `Price: $${item.price}`;
 	const stockSpan = document.createElement("span");
  	stockSpan.textContent = `Stock: ${item.stock}`;
 
	li.appendChild(nameh3);
  	li.appendChild(barcodeSpan);
  	li.appendChild(document.createElement("br"));
  	li.appendChild(priceSpan);
  	li.appendChild(document.createElement("br"));
  	li.appendChild(stockSpan);
   	document.querySelector("#item-list").appendChild(li);	
}

//PATCH:Update Stock Level
document.querySelector("#update-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const id = document.querySelector("#product-id").value;
  const updateStock = parseInt(document.querySelector("#update-stock").value);

  fetch(`http://127.0.0.1:5000/inventory/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({stock: updateStock})
  })
  .then(response => {
	if(!response.ok) {
		throw new Error("Error, response not ok");
	}
	return response.json();
  })
  .then(updatedItem => {
	console.log("Updated item:", updatedItem);
  })
  .catch(error => {
	console.error("Error:", error);
  });
});

//Delete Product
document.querySelector("#delete-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const id = (document.querySelector("#delete-product-id").value);

  fetch(`http://127.0.0.1:5000/inventory/${id}`, {
    method: "DELETE",
  })
  .then(response => {
	if(!response.ok) {
		throw new Error("Error, response not ok");
	}
	return response.json();
  })
  .then(data => {
	alert(data.message || "Product Deleted:");
  })
  .catch(error => {
	console.error("Error:", error);
  });
});

//View Enhanced Product Details by Barcode
document.querySelector("#enhance-form").addEventListener("submit", (e) => {
	e.preventDefault();
	const id = (document.querySelector("#enhance-product-id").value);

	fetch(`http://127.0.0.1:5000/inventory/${id}/enhance`, {
    	method: "GET",
    	headers: { "Content-Type": "application/json" },
  	})
  	.then(response => {
	if(!response.ok) {
		throw new Error("Error, response not ok");
	}
	return response.json();
  	})
	.then(data => {
		const enhancedDetails = document.querySelector("#enhanced-details")
		enhancedDetails.innerHTML = ""

		const brand = document.createElement("span");
		const ingredients = document.createElement("span")
		const allergens = document.createElement("span")
		
		brand.textContent = `Brand: ${data.brand}`;
		ingredients.textContent = `Ingredients: ${data.ingredients}`;
		allergens.textContent = `Allergens: ${data.allergens}`;

		enhancedDetails.appendChild(brand);
		enhancedDetails.appendChild(document.createElement("br"));
		enhancedDetails.appendChild(document.createElement("br"));
		enhancedDetails.appendChild(ingredients);
		enhancedDetails.appendChild(document.createElement("br"));
		enhancedDetails.appendChild(document.createElement("br"));
		enhancedDetails.appendChild(allergens)		
	})
   	.catch(error => {
	console.error("Error:", error);
  	});
})
 
