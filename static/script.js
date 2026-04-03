const socket = io();

let chart;
let aiChart;

// =======================
// 🔴 INITIAL STATUS
// =======================
document.getElementById("status").innerText = "🔴 Waiting for device...";

// =======================
// 📡 SOCKET LIVE DATA
// =======================
socket.on("connect", () => {
  console.log("✅ Socket Connected");
});

socket.on("sensor_update", (d) => {
  console.log("🔥 Live Data:", d);

  // Status
  document.getElementById("status").innerText = "🟢 Live Data";

  // Values update
  document.getElementById("temp").innerText = d.temperature;
  document.getElementById("hum").innerText = d.humidity;
  document.getElementById("gas").innerText = d.gas;
  document.getElementById("bat").innerText = d.battery;
  document.getElementById("risk").innerText = d.risk;

  // Heatmap update
  updateHeatmap(d.risk);
});

// =======================
// 🔥 HEATMAP ANIMATION
// =======================
function updateHeatmap(risk) {
  const box = document.getElementById("heatmap");

  box.style.transition = "all 0.5s ease";

  if (risk === "HIGH") {
    box.style.background = "linear-gradient(45deg, red, darkred)";
    box.innerText = "🔥 HIGH RISK";
  } 
  else if (risk === "MEDIUM") {
    box.style.background = "linear-gradient(45deg, orange, darkorange)";
    box.innerText = "⚠ MEDIUM RISK";
  } 
  else {
    box.style.background = "linear-gradient(45deg, green, darkgreen)";
    box.innerText = "✅ SAFE";
  }
}

// =======================
// 📊 INITIAL GRAPH LOAD
// =======================
async function loadChart() {
  try {
    const res = await fetch('/api/history');
    const data = await res.json();

    if (!data || data.length === 0) {
      console.log("No history data");
      return;
    }

    const labels = data.map((_, i) => i);
    const tempData = data.map(x => x.t);

    chart = new Chart(document.getElementById("chart"), {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Temperature',
          data: tempData,
          borderColor: '#38bdf8',
          tension: 0.4
        }]
      }
    });

  } catch (err) {
    console.log("Chart error:", err);
  }
}

loadChart();

// =======================
// 🔄 REAL-TIME GRAPH UPDATE
// =======================
setInterval(async () => {
  try {
    const res = await fetch('/api/history');
    const data = await res.json();

    if (!chart || !data) return;

    chart.data.labels = data.map((_, i) => i);
    chart.data.datasets[0].data = data.map(x => x.t);

    chart.update();

  } catch (err) {
    console.log("Update error:", err);
  }
}, 3000);

// =======================
// 🔮 AI PREDICTION GRAPH
// =======================
async function loadAI() {
  try {
    const res = await fetch('/api/predict');
    const json = await res.json();

    if (!json.data || json.data.length === 0) return;

    aiChart = new Chart(document.getElementById("aiChart"), {
      type: 'line',
      data: {
        labels: json.data.map(d => d.time),
        datasets: [{
          label: "Future Risk",
          data: json.data.map(d => d.risk),
          borderColor: '#f97316',
          borderDash: [5,5],
          tension: 0.4
        }]
      }
    });

  } catch (err) {
    console.log("AI error:", err);
  }
}

loadAI();

// =======================
// 🔄 AUTO REFRESH AI GRAPH (optional)
// =======================
setInterval(() => {
  loadAI();
}, 10000);
