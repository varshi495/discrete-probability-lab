(() => {
  const nInput = document.getElementById("n");
  const pInput = document.getElementById("p");
  const kInput = document.getElementById("k");
  const errorBox = document.getElementById("error");
  let chart;

  const fmt = (value, digits = 6) => {
    if (value === null || !Number.isFinite(value)) return "Not defined";
    return value.toFixed(digits);
  };

  // Draw a dashed vertical line at the mean without requiring an extra plugin.
  const meanLinePlugin = {
    id: "meanLine",
    afterDatasetsDraw(chartInstance, args, options) {
      if (options.mean === undefined || !chartInstance.chartArea) return;
      const {ctx, chartArea, scales} = chartInstance;
      const xScale = scales.x;
      const x = xScale.getPixelForValue(options.mean);
      if (x < chartArea.left || x > chartArea.right) return;
      ctx.save();
      ctx.beginPath();
      ctx.setLineDash([6, 5]);
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#e06b38";
      ctx.moveTo(x, chartArea.top);
      ctx.lineTo(x, chartArea.bottom);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = "#b64b20";
      ctx.font = "12px system-ui";
      ctx.fillText("Mean", Math.min(x + 6, chartArea.right - 36), chartArea.top + 13);
      ctx.restore();
    }
  };

  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = !message;
  }

  async function update() {
    const n = nInput.value;
    const p = pInput.value;
    const k = kInput.value;
    kInput.max = n || "20";
    document.getElementById("k-help").textContent =
      `Must be a whole number between 0 and ${n || "n"}.`;

    try {
      const response = await fetch("/api/binomial", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({n, p, k})
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Please check your inputs.");
      showError("");

      document.getElementById("selected").textContent = `n = ${data.n}, p = ${data.p}`;
      document.getElementById("mean").textContent = fmt(data.stats.mean, 4);
      document.getElementById("variance").textContent = fmt(data.stats.variance, 4);
      document.getElementById("sd").textContent = fmt(data.stats.standard_deviation, 4);
      document.getElementById("second").textContent = fmt(data.stats.second_moment, 4);
      document.getElementById("skewness").textContent = fmt(data.stats.skewness, 4);
      document.getElementById("pmf-k-label").textContent = data.k;
      document.getElementById("pmf").textContent = fmt(data.pmf, 8);
      document.getElementById("pmf-expression").textContent = `P(X = ${data.k})`;
      document.getElementById("cdf").textContent = fmt(data.cdf, 8);
      document.getElementById("complement").textContent = fmt(1 - data.cdf, 8);

      const labels = data.chart.map(point => point.x);
      const probabilities = data.chart.map(point => point.probability);
      if (chart) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = probabilities;
        chart.options.plugins.meanLine.mean = data.stats.mean;
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
          plugins: [meanLinePlugin],
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {mode: "index", intersect: false},
            plugins: {
              legend: {display: false},
              meanLine: {mean: data.stats.mean},
              tooltip: {
                callbacks: {
                  title: items => `X = ${items[0].label}`,
                  label: item => `P(X = ${item.label}) = ${Number(item.raw).toFixed(8)}`
                }
              }
            },
            scales: {
              x: {title: {display: true, text: "Number of successes X"}, grid: {display: false}},
              y: {beginAtZero: true, title: {display: true, text: "Probability P(X)"}, ticks: {callback: value => Number(value).toFixed(3)}}
            }
          }
        });
      }
    } catch (error) {
      showError(error.message);
    }
  }

  [nInput, pInput, kInput].forEach(input => input.addEventListener("input", update));
  update();
})();
