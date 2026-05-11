async function loadInventory() {

    // fetch inventory data
    const res = await fetch("/api/inventory");

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
                ${item.purchase_date}
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
                ${item.expiration_date}
            </td>

        </tr>
        `;
    });
}

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

// load inventory on page load
loadInventory();