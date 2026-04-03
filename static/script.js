
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
