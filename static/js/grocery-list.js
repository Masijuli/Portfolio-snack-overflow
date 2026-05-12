async function loadDropdown() {
    let res = await fetch("/api/grocery-lists");
    let items = await res.json();
    let select = document.getElementById("list_id");
    items.forEach(item => {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = item.value;
        select.appendChild(option);
    })

    let list = document.getElementById("list_id").value;
    if (!!list) {
        loadListItems(list);
    }
}

async function loadListItems(list) {
    let res = await fetch(`/api/grocery-lists/${list}/search`);
    let items = await res.json();
    const tableBody = document.getElementById("grocery-table-body");


    // clear existing rows
tableBody.innerHTML = "";

// generate rows
items.forEach(item => {

    const isPurchased = item.purchased === true;

    tableBody.innerHTML += `
        <tr class="${isPurchased ? "purchased-row" : ""}">

            <td class="food-cell">
                ${item.food}
            </td>

            <td class="notes-cell">
                ${item.notes || "-"}
            </td>

            <td class="quantity-cell">
                ${item.quantity} ${item.units || ""}
            </td>

            <td class="purchased-cell">
                ${
                    isPurchased
                    ? `<span class="purchased-label">Purchased</span>`
                    : `
                        <label class="purchase-checkbox-wrapper">
                            <input
                                type="checkbox"
                                onchange="markPurchased(${item.item_id})"
                            >
                            <span>Mark</span>
                        </label>
                    `
                }
            </td>

        </tr>
    `;
});
}

async function markPurchased(item_id) {
"/api/grocery-lists/<int:list_id>/mark"

    await fetch(
        `/api/grocery-lists/${item_id}/mark`,
        {
            method: "POST"
        }
    );

    let list = document.getElementById("list_id").value;
    if (!!list) {
        loadListItems(list);
    }
}

const addToListButton = document.getElementById("add-to-list-button");

addToListButton.addEventListener("click", async (e) => {
    let list = document.getElementById("list_id").value;
    if (!!list) {
        loadListItems(list);
    }
});

loadDropdown();