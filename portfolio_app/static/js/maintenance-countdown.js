(() => {
    const timer = document.querySelector("[data-reopen-at]");
    const countdown = document.getElementById("reopen-countdown");
    if (!timer || !countdown) return;

    const reopenAt = Date.parse(timer.dataset.reopenAt);
    if (!Number.isFinite(reopenAt)) return;

    let reopening = false;
    async function updateCountdown() {
        const secondsRemaining = Math.max(
            0,
            Math.ceil((reopenAt - Date.now()) / 1000)
        );
        const hours = Math.floor(secondsRemaining / 3600);
        const minutes = Math.floor((secondsRemaining % 3600) / 60);
        const seconds = String(secondsRemaining % 60).padStart(2, "0");
        countdown.textContent = hours
            ? `${hours}:${String(minutes).padStart(2, "0")}:${seconds}`
            : `${minutes}:${seconds}`;

        if (secondsRemaining || reopening) return;
        reopening = true;
        try {
            const response = await fetch("/api/site-heartbeat/", {
                credentials: "same-origin",
            });
            if (!response.ok) {
                throw new Error(`Availability check failed (${response.status}).`);
            }
            const status = await response.json();
            if (status.enabled) {
                reopening = false;
                window.setTimeout(updateCountdown, 1000);
                return;
            }
            window.location.reload();
        } catch (error) {
            console.error("Could not restore the website automatically.", error);
            reopening = false;
            window.setTimeout(updateCountdown, 5000);
        }
    }

    updateCountdown();
    window.setInterval(updateCountdown, 1000);
})();
