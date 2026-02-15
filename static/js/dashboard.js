const speedDisplay = document.getElementById("speed");
const rpmDisplay = document.getElementById("rpm");
const throttleDisplay = document.getElementById("throttle");
const tempDisplay = document.getElementById("temp");
const modeDisplay = document.getElementById("mode");
const confidenceDisplay = document.getElementById("confidence");
const explanationDisplay = document.getElementById("explanation");

let index = 0;
let speedLabels = [];
let speedData = [];
let rpmLabels = [];
let rpmData = [];
let dynamicMaxRPM = 8000;

// -------- SPEED CHART --------
const speedChart = new Chart(
    document.getElementById("speedChart"),
    {
        type: "line",
        data: {
            labels: speedLabels,
            datasets: [{
                label: "Speed (km/h)",
                data: speedData,
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            animation: false,
            scales: {
                y: {
                    min: 0,
                    max: 200
                }
            }
        }
    }
);

// -------- RPM CHART --------
const rpmChart = new Chart(
    document.getElementById("rpmChart"),
    {
        type: "line",
        data: {
            labels: rpmLabels,
            datasets: [{
                label: "RPM",
                data: rpmData,
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            animation: false,
            scales: {
                y: {
                    min: 0,
                    max: dynamicMaxRPM
                }
            }
        }
    }
);

// -------- SSE CONNECTION --------
const source = new EventSource("/api/stream");

source.onmessage = function (event) {
    const data = JSON.parse(event.data);

    const speed = Number(data.speed) || 0;
    const rpm = Number(data.rpm) || 0;
    const throttle = Number(data.throttle_pos) || 0;
    const temp = Number(data.coolant_temp) || 0;

    speedDisplay.innerText = speed.toFixed(1) + " km/h";
    rpmDisplay.innerText = rpm.toFixed(0);
    throttleDisplay.innerText = throttle.toFixed(1) + " %";
    tempDisplay.innerText = temp.toFixed(1) + " °C";

    modeDisplay.innerText = data.driving_mode || "Unknown";
    confidenceDisplay.innerText = "Confidence: " + (data.ai_confidence || 0) + " %";

    if (data.explanation) {
        explanationDisplay.innerText = data.explanation.join(", ");
    }

    // Dynamic RPM scaling
    if (data.max_rpm && data.max_rpm > dynamicMaxRPM) {
        dynamicMaxRPM = data.max_rpm + 500;
        rpmChart.options.scales.y.max = dynamicMaxRPM;
    }

    speedLabels.push(index);
    speedData.push(speed);
    rpmLabels.push(index);
    rpmData.push(rpm);
    index++;

    if (speedLabels.length > 40) {
        speedLabels.shift();
        speedData.shift();
        rpmLabels.shift();
        rpmData.shift();
    }

    speedChart.update("none");
    rpmChart.update("none");

    // Mode color coding
    if (data.driving_mode === "Smooth") {
        modeDisplay.style.color = "#00ff88";
    } else if (data.driving_mode === "Normal") {
        modeDisplay.style.color = "#ffff00";
    } else if (data.driving_mode === "Aggressive") {
        modeDisplay.style.color = "#ff8800";
    } else {
        modeDisplay.style.color = "#ff0000";
    }
};

source.onerror = function () {
    console.error("SSE connection lost");
};
