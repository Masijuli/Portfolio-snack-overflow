
async function loadDashboard() {
    let container;

    let response = await fetch("/api/dashboard");
    let items = await response.json();
    container = document.getElementById("dashboard-inventory");
    container.innerHTML = `${items.inventory_count}`;

    container = document.getElementById("dashboard-expired");
    container.innerHTML = `${items.expired_count}`;

    container = document.getElementById("dashboard-expiring-7");
    container.innerHTML = `${items.expiring_7_count}`;

    container = document.getElementById("dashboard-open");
    container.innerHTML = `${items.open_count}`;

    container = document.getElementById("dashboard-recipes");
    container.innerHTML = `${items.recipes_count}`;
}

async function loadAttetion() {
    let responseExpired = await fetch ("/api/dashboard/expired-list");
    let itemsExpired = await responseExpired.json();
    let responseExpiring7 = await fetch ("/api/dashboard/expiring-7-list");
    let itemsExpiring7 = await responseExpiring7.json();
    let container = document.getElementById("attention");

    if (itemsExpired.length == 0 && itemsExpiring7.length == 0) {
        container.innerHTML = ` <p>
                                    Nothing expiring soon. 🎉
                                </p>`;
    } else {
        let inner = "<ul>"
        for (let i of itemsExpired) {
            let date = new Date(i.expiration);
            dateFormatted = date.toLocaleDateString("en-US", {
                month: "numeric",
                day: "numeric",
                year: "numeric"
            });
            inner += `<li class="expired"><b>${i.name}</b> expired on <b>${dateFormatted}</b></li>`;
        }
        for (let i of itemsExpiring7) {
            let date = new Date(i.expiration);
            dateFormatted = date.toLocaleDateString("en-US", {
                month: "numeric",
                day: "numeric",
                year: "numeric"
            });
            inner += `<li class="expiring7"><b>${i.name}</b> expires on <b>${dateFormatted}</b></li>`;
        }
        inner += "</ul>";
        container.innerHTML = inner;
    }
}

loadDashboard();
loadAttetion();