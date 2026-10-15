(() => {
  const pInput = document.getElementById("p");
  const kInput = document.getElementById("k");
  const errorBox = document.getElementById("error");
  let chart;

  const fmt = (value, digits = 6) => {
    if (value === null || !Number.isFinite(value)) return "Not defined";
    return value.toFixed(digits);
  };
  const fmtProbability = value => {
    if (!Number.isFinite(value)) return "Not defined";
    return value > 0 && value < 1e-6 ? value.toExponential(1) : value.toFixed(8);
  };
  const fmtCdf = (value, complement) => {
    if (complement > 0 && Number(value.toFixed(8)) === 1) {
      return `1 - ${fmtProbability(complement)}`;
    }
    return fmtProbability(value);
  };

  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = !message;
  }

  async function update() {
    const p = pInput.value;
    const k = kInput.value;

    try {
      const response = await fetch("/api/geometric", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({p, k})
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Please check your inputs.");
      showError("");

      document.getElementById("selected").textContent = `p = ${data.p}`;
      document.getElementById("mean").textContent = fmt(data.stats.mean, 4);
      document.getElementById("variance").textContent = fmt(data.stats.variance, 4);
      document.getElementById("sd").textContent = fmt(data.stats.standard_deviation, 4);
      document.getElementById("second").textContent = fmt(data.stats.second_moment, 4);
      document.getElementById("skewness").textContent = fmt(data.stats.skewness, 4);
      document.getElementById("pmf-k-label").textContent = data.k;
      document.getElementById("pmf").textContent = fmtProbability(data.pmf);
      document.getElementById("pmf-expression").textContent = `P(X = ${data.k})`;
      document.getElementById("cdf").textContent = fmtCdf(data.cdf, data.complement);
      document.getElementById("complement").textContent = fmtProbability(data.complement);

      const labels = data.chart.map(point => point.x);
      const probabilities = data.chart.map(point => point.probability);
      if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = probabilities;
        chart.update();
      } else {
        chart = new Chart(document.getElementById("pmfChart"), {
          type: "bar",
          data: {
            labels,
            datasets: [{
              label: "P(X = k)",
              data: probabilities,
              backgroundColor: "#7188ed",
              hoverBackgroundColor: "#3659d9",
              borderRadius: 4,
              maxBarThickness: 34
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {mode: "index", intersect: false},
            plugins: {
              legend: {display: false},
              tooltip: {
                callbacks: {
                  title: items => `X = ${items[0].label}`,
                  label: item => `P(X = ${item.label}) = ${fmtProbability(Number(item.raw))}`
                }
              }
            },
            scales: {
              x: {title: {display: true, text: "Trial of first success X"}, grid: {display: false}},
              y: {beginAtZero: true, title: {display: true, text: "Probability P(X)"}, ticks: {callback: value => Number(value).toFixed(3)}}
            }
          }
        });
      }
    } catch (error) {
      showError(error.message);
    }
  }

  [pInput, kInput].forEach(input => input.addEventListener("input", update));
  update();
})();
