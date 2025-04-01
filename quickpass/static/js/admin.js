function expandChart(chart) {
    const overlay = document.getElementById("overlay");
    const closeBtn = chart.querySelector(".close-btn");

    if (chart.classList.contains("expand")) {
        closeChart(chart);
        return;
    }

    document.querySelectorAll(".chart-container").forEach(c => {
        if (c.classList.contains("expand")) {
            closeChart(c);
        }
    });

    chart.classList.add("expand");
    overlay.style.display = "block";

    closeBtn.onclick = (event) => {
        closeChart(chart);
        event.stopPropagation();
    };

    overlay.onclick = () => {
        closeChart(chart);
    };
}

function closeChart(chart) {
    chart.classList.remove("expand");
    document.getElementById("overlay").style.display = "none";
}

// Agregar eventos a los gráficos
document.querySelectorAll(".chart-container").forEach(chart => {
    chart.addEventListener("click", (event) => {
        expandChart(chart);
        event.stopPropagation();
    });
});