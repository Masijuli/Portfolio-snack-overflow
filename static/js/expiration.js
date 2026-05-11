
async function loadExpiration() {
    let container;

    let response = await fetch("/api/dashboard");
    let items = await response.json();

    container = document.getElementById("expired");
    container.innerHTML = `${items.expired_count}`;

    container = document.getElementById("expiring-7");
    container.innerHTML = `${items.expiring_7_count}`;
}

async function loadExpiationLists() {
    let responseExpired = await fetch ("/api/expired-list");
    let itemsExpired = await responseExpired.json();
    let containerExpired = document.getElementById("expired-list");
    let responseExpiring7 = await fetch ("/api/expiring-7-list");
    let itemsExpiring7 = await responseExpiring7.json();
    let containerExpiring7 = document.getElementById("expiring-7-list");

    if (itemsExpired.length == 0) {
        containerExpired.innerHTML = ` <p>
                                    Nothing expired. 🎉
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
        inner += "</ul>";
        containerExpired.innerHTML = inner;
    }
    
    if (itemsExpiring7.length == 0) {
        containerExpiring7.innerHTML = ` <p>
                                    Nothing expiring soon. 🎉
                                </p>`;
    } else {
        let inner = "<ul>"
        for (let i of itemsExpiring7) {
            let date = new Date(i.expiration);
            dateFormatted = date.toLocaleDateString("en-US", {
                month: "numeric",
                day: "numeric",
                year: "numeric"
            });
            inner += `<li class="expiring7"><b>${i.name}</b> expiring on <b>${dateFormatted}</b></li>`;
        }
        inner += "</ul>";
        containerExpiring7.innerHTML = inner;
    }
}

loadExpiration();
loadExpiationLists();