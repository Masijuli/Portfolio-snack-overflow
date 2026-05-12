async function loadInventory(api_call = "/api/inventory") {

    // fetch inventory data
    const res = await fetch(api_call);

    const items = await res.json();

    // table body
    const tableBody =
        document.getElementById("inventory-table-body");

    // clear existing rows
    tableBody.innerHTML = "";

    // generate rows
    items.forEach(item => {

        const purchaseDate =
            item.purchase_date
                ? new Date(item.purchase_date).toLocaleDateString()
                : "-";

        const openedDate =
            item.opened_date
                ? new Date(item.opened_date).toLocaleDateString()
                : "Unopened";

        const expirationDate =
            item.expiration_date
                ? new Date(item.expiration_date).toLocaleDateString()
                : "-";

        const is_opened = item.opened_date ? "opened" : "unopened";

        tableBody.innerHTML += `

        <tr>

            <td class="food-name">
                ${item.name}
            </td>

            <td class="quantity-cell">
                ${item.quantity} ${item.unit}
            </td>

            <td class="storage-cell">
                ${item.storage || "-"}
            </td>

            <td class="store-cell">
                ${item.store || "-"}
            </td>

            <td class="date-cell">
                ${new Date(item.purchase_date).toLocaleDateString()}
            </td>

            <td class="opened-cell">
            ${
                item.opened_date
                ?
                new Date(item.opened_date).toLocaleDateString()
                :
                `
                <label class="open-checkbox-wrapper">

                    <input
                        type="checkbox"
                        class="open-checkbox"
                        onchange="openItem(${item.inventory_id})"
                    >

                    <span>Open</span>

                </label>
                `
            }
            </td>

            <td class="expiration-date">
                ${new Date(item.expiration_date).toLocaleDateString()}
            </td>

        </tr>
        `;
    });
}

async function loadDropdown() {
    let res, items, select;
    let endpoints = [["/api/foods", "food_id"],
                    ["/api/stores", "store_id"],
                    ["/api/storage", "storage_id"],
                    ["/api/units", "unit_id"]];
    for (let i = 0; i < endpoints.length; i++) {
        res = await fetch(endpoints[i][0]);
        items = await res.json();
        select = document.getElementById(endpoints[i][1]);
        items.forEach(item => {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item.value;
            select.appendChild(option);
        })
    }
}

// updates database when an item is clicked that it has been opened
async function openItem(inventory_id) {

    await fetch(
        `/api/inventory/${inventory_id}/open`,
        {
            method: "POST"
        }
    );

    // reload inventory table
    loadInventory();
}

const modal = document.getElementById("inventory-modal");
const openBtn = document.getElementById("add-item-btn");
const closeBtn = document.getElementById("close-modal");

// OPEN MODAL
openBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
});

// CLOSE MODAL
closeBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
});

// close when clicking outside modal
modal.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.classList.add("hidden");
    }
});

document.getElementById("inventory-form").addEventListener("submit", async (e) => {

    e.preventDefault();

    const payload = {
        food_id: document.getElementById("food_id").value,
        storage_id: document.getElementById("storage_id").value,
        // purchase_price, COME BACK HERE
        expiration_date: document.getElementById("expiration_date").value,
        opened_date: null,
        quantity: document.getElementById("quantity").value,
        unit_id: document.getElementById("unit_id").value,
        run_id: document.getElementById("store_id").value,
        purchase_date: new Date()
        
    };
    console.log(payload);

    await fetch("/api/inventory", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    modal.classList.add("hidden");

    loadInventory(); // refresh table
});

document.getElementById("search-button").addEventListener("click", async (e) => {
    let search = document.getElementById("search-input").value;
    if (!!search) {
        loadInventory(`/api/inventory/${search}/search`);
    } else {
        loadInventory();
    }
})

// load inventory on page load
loadInventory();
loadDropdown();