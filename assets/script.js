let mainLabelAliasMap = {};

// 載入 aliasMap.json
fetch('assets/aliasMap.json')
  .then(response => response.json())
  .then(data => {
    mainLabelAliasMap = data;
  })
  .catch(err => {
    console.error('無法載入 aliasMap.json:', err);
  });

window.onload = function () {
  fetch('output/result.json')
    .then(response => response.json())
    .then(data => renderPredictions(data))
    .catch(err => {
      document.getElementById('output').innerHTML = 
        `<p style="color:red;">無法載入 JSON：${err}</p>`;
      console.error(err);
    });
};

// 傳回別名的函式
function getAliasForMainLabel(mainLabel) {
  return mainLabelAliasMap[mainLabel] || mainLabel;
}

function renderPredictions(data) {
  const output = document.getElementById('output');
  output.innerHTML = '';

  const predictions = data.predictions;

  predictions.forEach((prediction, idx) => {
    const container = document.createElement('div');
    container.className = 'result';

    const header = document.createElement('h2');
    header.textContent = `預測結果 #${idx + 1}`;
    container.appendChild(header);

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    container.appendChild(canvas);

    const parts = prediction.prediction.split(';');
    const classificationOnly = parts.slice(1);
    const label = classificationOnly.pop();
    const scaleFactor = 0.2;

    const img = new Image();
    img.onload = function () {
      canvas.width = img.width * scaleFactor;
      canvas.height = img.height * scaleFactor;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      const detections = prediction.detections || [];
      detections.sort((a, b) => a.conf - b.conf);

      detections.forEach(det => {
        const [xmin, ymin, width, height] = det.bbox;
        const conf = det.conf;

        const x = xmin * img.width * scaleFactor;
        const y = ymin * img.height * scaleFactor;
        const w = width * img.width * scaleFactor;
        const h = height * img.height * scaleFactor;

        const alpha = Math.max(conf, 0.1);
        const color = getColor(label, alpha);

        // 畫框
        ctx.lineWidth = 8;
        ctx.font = "bold 200px sans-serif";
        ctx.strokeStyle = color;
        ctx.strokeRect(x, y, w, h);

        const text = `${label}: ${conf.toFixed(2)}`;
        ctx.font = "bold 14px sans-serif";
        const textWidth = ctx.measureText(text).width;
        const textHeight = 18;

        ctx.fillStyle = color;
        ctx.fillRect(x, y - textHeight, textWidth + 6, textHeight);

        // 畫文字
        ctx.fillStyle = `rgba(255,255,255,${alpha})`;
        ctx.fillText(text, x + 3, y - 4);
      });
    };

    img.src = prediction.filepath;

    // 預測結果資訊
    const predTitle = document.createElement('h3');
    predTitle.innerText = '主要預測';
    container.appendChild(predTitle);

    const predText = document.createElement('p');
    const mainLabel = prediction.prediction.split(';').pop();
    const alias = getAliasForMainLabel(mainLabel);
    predText.innerHTML = `<strong>預測：</strong> ${alias}<br>
                          <strong>信心分數：</strong> ${prediction.prediction_score.toFixed(4)}<br>
                          <strong>來源：</strong> ${prediction.prediction_source}<br>
                          <strong>模型版本：</strong> ${prediction.model_version}`;
    container.appendChild(predText);

    // 類別列表
    const classTitle = document.createElement('h3');
    classTitle.innerText = '分類結果';
    container.appendChild(classTitle);

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = `<tr><th>分類路徑</th><th>信心分數</th></tr>`;
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    prediction.classifications.classes.forEach((cls, index) => {
      const row = document.createElement('tr');
      const label = cls.split(';').slice(1).join(' > ');
      const score = prediction.classifications.scores[index].toFixed(4);

      if (parseFloat(score) > 0.8) {
        row.style.backgroundColor = 'yellow';
      }

      row.innerHTML = `<td>${label}</td><td>${score}</td>`;
      tbody.appendChild(row);
    });
    table.appendChild(tbody);
    container.appendChild(table);

    output.appendChild(container);
  });
}

// 顏色對應表，自己加要顯示的顏色
const DETECTIONS_COLOR_MAP = {
  animal: "255,0,0"
};

function getColor(label, alpha = 1.0) {
  const rgb = DETECTIONS_COLOR_MAP[label] || "255,255,0"; // 預設黃色
  return `rgba(${rgb},${alpha})`;
}