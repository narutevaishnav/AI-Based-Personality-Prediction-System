// ==========================================
// HISTORY PAGE JAVASCRIPT
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    // ==========================================
    // SEARCH HISTORY
    // ==========================================

    const searchInput = document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const value = this.value.toLowerCase();

            const rows = document.querySelectorAll("tbody tr");

            rows.forEach((row) => {

                const text = row.innerText.toLowerCase();

                row.style.display = text.includes(value) ? "" : "none";

            });

        });

    }

    // ==========================================
    // DELETE CONFIRMATION
    // ==========================================

    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach((btn) => {

        btn.addEventListener("click", function (e) {

            const ok = confirm(
                "Are you sure you want to delete this prediction?"
            );

            if (!ok) {

                e.preventDefault();

            }

        });

    });

    // ==========================================
    // TABLE FADE ANIMATION
    // ==========================================

    const rows = document.querySelectorAll("tbody tr");

    rows.forEach((row, index) => {

        row.style.opacity = "0";
        row.style.transform = "translateY(20px)";

        setTimeout(() => {

            row.style.transition = "0.5s ease";

            row.style.opacity = "1";
            row.style.transform = "translateY(0px)";

        }, index * 100);

    });

    // ==========================================
    // ACTION BUTTON HOVER
    // ==========================================

    const buttons = document.querySelectorAll(".action-btn");

    buttons.forEach((btn) => {

        btn.addEventListener("mouseenter", () => {

            btn.style.transform = "scale(1.12)";

        });

        btn.addEventListener("mouseleave", () => {

            btn.style.transform = "scale(1)";

        });

    });

    // ==========================================
    // SEARCH CLEAR ON ESC
    // ==========================================

    if (searchInput) {

        searchInput.addEventListener("keydown", function (e) {

            if (e.key === "Escape") {

                this.value = "";

                document.querySelectorAll("tbody tr").forEach((row) => {

                    row.style.display = "";

                });

            }

        });

    }

});