
const socket = io();
socket.on("sensor_update", d=>{
 document.getElementById("status").innerText="Live";
});

fetch('/api/history').then(r=>r.json()).then(data=>{
 new Chart(document.getElementById("chart"),{
  type:'line',
  data:{labels:data.map((_,i)=>i),datasets:[{data:data.map(x=>x.t)}]}
 });
});

async function loadAI() {
    const res = await fetch('/api/predict');
    const json = await res.json();

    if (json.data.length === 0) return;

    new Chart(document.getElementById("aiChart"), {
        type: 'line',
        data: {
            labels: json.data.map(d => d.time),
            datasets: [{
                label: "Future Risk",
                data: json.data.map(d => d.risk),
                borderDash: [5,5]
            }]
        }
    });
}

loadAI();
