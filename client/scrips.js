fetch("http://127.0.0.1:5000/inventory")
  .then(response => response.json())
  .then(events => {
    events.forEach(renderItem);
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
  .then(renderItem);
});

function renderItem(item) {
//   console.log(item)
  const li = document.createElement("li");
  li.textContent = `${item.name}`;
  document.querySelector("#item-list").appendChild(li);
}