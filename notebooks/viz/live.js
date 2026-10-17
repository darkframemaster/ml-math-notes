function svgEl(name, attrs) {
  const node = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [key, value] of Object.entries(attrs || {})) {
    node.setAttribute(key, String(value));
  }
  return node;
}

function clamp(value, lo, hi) {
  return Math.max(lo, Math.min(hi, value));
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function rgb(r, g, b) {
  return `rgb(${r | 0},${g | 0},${b | 0})`;
}

function diverging(t) {
  const x = clamp(t, 0, 1);
  if (x < 0.5) {
    const u = x / 0.5;
    return rgb(lerp(178, 247, u), lerp(24, 247, u), lerp(43, 247, u));
  }
  const u = (x - 0.5) / 0.5;
  return rgb(lerp(247, 33, u), lerp(247, 102, u), lerp(247, 172, u));
}

function sequential(t) {
  const x = clamp(t, 0, 1);
  return rgb(lerp(247, 33, x), lerp(251, 113, x), lerp(255, 181, x));
}

function viridis(t) {
  const x = clamp(t, 0, 1);
  return rgb(
    lerp(68, 253, x) * (x < 0.5 ? lerp(0.4, 1, x / 0.5) : 1),
    lerp(1, 231, x),
    lerp(84, 37, x),
  );
}

function mountControls(parent, controls, state, onInput) {
  const bar = document.createElement("div");
  bar.style.cssText = "display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;margin:4px 0 8px;font:13px/1.2 -apple-system,BlinkMacSystemFont,sans-serif;color:#222;";
  for (const control of controls || []) {
    if (control.type === "button") {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = control.label;
      button.style.cssText = "padding:4px 10px;border:1px solid #ccc;border-radius:4px;background:#fff;cursor:pointer;";
      button.addEventListener("click", () => onInput(control.name));
      bar.appendChild(button);
      continue;
    }
    if (control.type === "checkbox") {
      const label = document.createElement("label");
      label.style.cssText = "display:inline-flex;align-items:center;gap:6px;";
      const input = document.createElement("input");
      input.type = "checkbox";
      input.checked = !!control.value;
      state[control.name] = !!control.value;
      input.addEventListener("change", () => {
        state[control.name] = input.checked;
        onInput(control.name);
      });
      label.append(input, document.createTextNode(control.label));
      bar.appendChild(label);
      continue;
    }
    if (control.type === "select") {
      const label = document.createElement("label");
      label.style.cssText = "display:inline-flex;align-items:center;gap:6px;";
      label.appendChild(document.createTextNode(control.label));
      const select = document.createElement("select");
      for (const option of control.options) {
        const node = document.createElement("option");
        node.value = String(option.value);
        node.textContent = option.label;
        select.appendChild(node);
      }
      select.value = String(control.value);
      state[control.name] = Number(control.value);
      select.addEventListener("change", () => {
        state[control.name] = Number(select.value);
        onInput(control.name);
      });
      label.appendChild(select);
      bar.appendChild(label);
      continue;
    }
    const label = document.createElement("label");
    label.style.cssText = "display:inline-flex;align-items:center;gap:8px;";
    const name = document.createElement("span");
    name.textContent = control.label;
    name.style.minWidth = "48px";
    const input = document.createElement("input");
    input.type = "range";
    input.min = control.min;
    input.max = control.max;
    input.step = control.step;
    input.value = control.value;
    input.style.width = "180px";
    const digits = control.digits ?? 2;
    const readout = document.createElement("span");
    readout.style.minWidth = "44px";
    readout.textContent = Number(control.value).toFixed(digits);
    state[control.name] = Number(control.value);
    input.addEventListener("input", () => {
      state[control.name] = Number(input.value);
      readout.textContent = state[control.name].toFixed(digits);
      onInput(control.name);
    });
    label.append(name, input, readout);
    bar.appendChild(label);
  }
  parent.appendChild(bar);
}

function scatterFrame(host, title) {
  host.replaceChildren();
  const width = 720;
  const height = 460;
  const pad = { l: 48, r: 16, t: 36, b: 40 };
  const svg = svgEl("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
  svg.style.cssText = "background:#fff;border:1px solid #eee;max-width:100%;height:auto;";
  svg.appendChild(svgEl("text", { x: 16, y: 22, "font-size": 14, fill: "#222" })).textContent = title;
  host.appendChild(svg);
  return {
    svg,
    pad,
    width,
    height,
    plotW: width - pad.l - pad.r,
    plotH: height - pad.t - pad.b,
  };
}

function mapPoint(frame, x, y, xmin, xmax, ymin, ymax) {
  return [
    frame.pad.l + ((x - xmin) / (xmax - xmin)) * frame.plotW,
    frame.pad.t + ((ymax - y) / (ymax - ymin)) * frame.plotH,
  ];
}

function drawAxes(frame, xmin, xmax, ymin, ymax) {
  const axis = svgEl("g", { stroke: "#ccc", "stroke-width": 1 });
  for (const tick of [-3, -1.5, 0, 1.5, 3]) {
    const [x] = mapPoint(frame, tick, 0, xmin, xmax, ymin, ymax);
    const [, y] = mapPoint(frame, 0, tick, xmin, xmax, ymin, ymax);
    axis.appendChild(svgEl("line", { x1: x, y1: frame.pad.t, x2: x, y2: frame.pad.t + frame.plotH }));
    axis.appendChild(svgEl("line", { x1: frame.pad.l, y1: y, x2: frame.pad.l + frame.plotW, y2: y }));
    const xt = svgEl("text", { x, y: frame.height - 16, "text-anchor": "middle", "font-size": 11, fill: "#666", stroke: "none" });
    xt.textContent = String(tick);
    const yt = svgEl("text", { x: 8, y: y + 4, "font-size": 11, fill: "#666", stroke: "none" });
    yt.textContent = String(tick);
    frame.svg.append(xt, yt);
  }
  frame.svg.appendChild(axis);
}

function paintNeuron(host, payload, state) {
  const w1 = state.w1;
  const w2 = state.w2;
  const bias = state.bias;
  const frame = scatterFrame(host, `决策边界：${w1.toFixed(2)}·x1 + ${w2.toFixed(2)}·x2 + ${bias.toFixed(2)} = 0`);
  const xmin = -3.5;
  const xmax = 3.5;
  drawAxes(frame, xmin, xmax, xmin, xmax);
  const dots = svgEl("g");
  payload.x0.forEach((x, i) => {
    const [cx, cy] = mapPoint(frame, x, payload.y0[i], xmin, xmax, xmin, xmax);
    dots.appendChild(svgEl("circle", { cx, cy, r: 4, fill: "#4C78A8", "fill-opacity": 0.75 }));
  });
  payload.x1.forEach((x, i) => {
    const [cx, cy] = mapPoint(frame, x, payload.y1[i], xmin, xmax, xmin, xmax);
    dots.appendChild(svgEl("circle", { cx, cy, r: 4, fill: "#F58518", "fill-opacity": 0.75 }));
  });
  frame.svg.appendChild(dots);
  let x1;
  let y1;
  let x2;
  let y2;
  if (Math.abs(w2) < 1e-3) {
    const x = -bias / (w1 + 1e-9);
    [x1, y1] = mapPoint(frame, x, xmin, xmin, xmax, xmin, xmax);
    [x2, y2] = mapPoint(frame, x, xmax, xmin, xmax, xmin, xmax);
  } else {
    const xs = [xmin, xmax];
    const ys = xs.map((x) => (-(w1 / w2)) * x - bias / w2);
    [x1, y1] = mapPoint(frame, xs[0], ys[0], xmin, xmax, xmin, xmax);
    [x2, y2] = mapPoint(frame, xs[1], ys[1], xmin, xmax, xmin, xmax);
  }
  frame.svg.appendChild(svgEl("line", {
    x1, y1, x2, y2, stroke: "#E45756", "stroke-width": 3,
  }));
}

function softmaxProbs(logits, temperature) {
  const scaled = logits.map((value) => value / Math.max(temperature, 1e-6));
  const peak = Math.max(...scaled);
  const exps = scaled.map((value) => Math.exp(value - peak));
  const total = exps.reduce((sum, value) => sum + value, 0);
  return exps.map((value) => value / total);
}

function paintSoftmax(host, payload, state) {
  const probs = softmaxProbs(payload.logits, state.temperature);
  host.replaceChildren();
  const width = 700;
  const height = 380;
  const svg = svgEl("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
  svg.style.cssText = "background:#fff;border:1px solid #eee;max-width:100%;height:auto;";
  svg.appendChild(svgEl("text", { x: 16, y: 22, "font-size": 14, fill: "#222" })).textContent =
    `Softmax(logits / T)，T = ${state.temperature.toFixed(2)}`;
  const pad = { l: 48, r: 16, t: 40, b: 40 };
  const plotW = width - pad.l - pad.r;
  const plotH = height - pad.t - pad.b;
  const gap = 12;
  const barW = (plotW - gap * (probs.length - 1)) / probs.length;
  probs.forEach((prob, index) => {
    const h = prob * plotH;
    const x = pad.l + index * (barW + gap);
    const y = pad.t + plotH - h;
    svg.appendChild(svgEl("rect", { x, y, width: barW, height: h, fill: "#54A24B" }));
    const label = svgEl("text", { x: x + barW / 2, y: height - 16, "text-anchor": "middle", "font-size": 12, fill: "#444" });
    label.textContent = payload.labels[index];
    svg.appendChild(label);
    const value = svgEl("text", { x: x + barW / 2, y: y - 6, "text-anchor": "middle", "font-size": 11, fill: "#222" });
    value.textContent = prob.toFixed(2);
    svg.appendChild(value);
  });
  host.appendChild(svg);
}

function sinusoidal(seqLen, dModel) {
  const rows = [];
  for (let pos = 0; pos < seqLen; pos += 1) {
    const row = [];
    for (let dim = 0; dim < dModel; dim += 1) {
      const half = Math.floor(dim / 2);
      const div = Math.exp(half * (-Math.log(10000) / dModel));
      row.push(dim % 2 === 0 ? Math.sin(pos * div) : Math.cos(pos * div));
    }
    rows.push(row);
  }
  return rows;
}

function paintPositional(host, payload, state) {
  const pe = sinusoidal(payload.maxLen, payload.dModel);
  const pos = state.pos | 0;
  const dim = state.dim | 0;
  host.replaceChildren();
  const heat = document.createElement("canvas");
  const cell = 8;
  heat.width = payload.maxLen * cell + 8;
  heat.height = payload.dModel * cell + 8;
  heat.style.cssText = "max-width:100%;background:#fff;border:1px solid #eee;";
  const ctx = heat.getContext("2d");
  for (let d = 0; d < payload.dModel; d += 1) {
    for (let p = 0; p < payload.maxLen; p += 1) {
      ctx.fillStyle = diverging((pe[p][d] + 1) / 2);
      ctx.fillRect(p * cell, d * cell, cell, cell);
    }
  }
  ctx.strokeStyle = "#E45756";
  ctx.strokeRect(pos * cell + 0.5, 0.5, cell - 1, payload.dModel * cell - 1);
  const wave = document.createElement("canvas");
  wave.width = 720;
  wave.height = 220;
  wave.style.cssText = "display:block;margin-top:8px;background:#fff;border:1px solid #eee;max-width:100%;";
  const g = wave.getContext("2d");
  g.fillStyle = "#222";
  g.font = "14px sans-serif";
  g.fillText(`维度 dim=${dim} 的波形；红点 = pos=${pos}`, 12, 20);
  g.beginPath();
  g.strokeStyle = "#4C78A8";
  g.lineWidth = 2;
  for (let p = 0; p < payload.maxLen; p += 1) {
    const x = 40 + (p / (payload.maxLen - 1)) * 660;
    const y = 120 - pe[p][dim] * 70;
    if (p === 0) g.moveTo(x, y);
    else g.lineTo(x, y);
  }
  g.stroke();
  const px = 40 + (pos / (payload.maxLen - 1)) * 660;
  const py = 120 - pe[pos][dim] * 70;
  g.fillStyle = "#E45756";
  g.beginPath();
  g.arc(px, py, 5, 0, Math.PI * 2);
  g.fill();
  const next = Math.min(pos + 1, payload.maxLen - 1);
  const a = pe[pos];
  const b = pe[next];
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  const cos = dot / (Math.sqrt(na) * Math.sqrt(nb) + 1e-9);
  const note = document.createElement("div");
  note.style.cssText = "margin-top:6px;font:13px sans-serif;";
  note.textContent = `PE[pos=${pos}] 的 L2 范数 = ${Math.sqrt(na).toFixed(3)}；与下一位置的余弦相似度 = ${cos.toFixed(3)}`;
  host.append(heat, wave, note);
}

function paintAttention(host, payload, state) {
  const q = state.query | 0;
  const row = payload.weights[q];
  host.replaceChildren();
  const width = 720;
  const height = 340;
  const svg = svgEl("svg", { width, height, viewBox: `0 0 ${width} ${height}` });
  svg.style.cssText = "background:#fff;border:1px solid #eee;max-width:100%;height:auto;";
  svg.appendChild(svgEl("text", { x: 16, y: 22, "font-size": 14, fill: "#222" })).textContent =
    `Query = 「${payload.tokens[q]}」的注意力分布`;
  const max = Math.max(0.5, ...payload.weights.flat());
  const pad = { l: 40, r: 12, t: 36, b: 36 };
  const plotH = height - pad.t - pad.b;
  const barW = (width - pad.l - pad.r) / row.length;
  row.forEach((value, index) => {
    const h = (value / (max * 1.15)) * plotH;
    const x = pad.l + index * barW + 4;
    const y = pad.t + plotH - h;
    svg.appendChild(svgEl("rect", {
      x, y, width: barW - 8, height: h, fill: index === q ? "#F58518" : "#4C78A8",
    }));
    const label = svgEl("text", { x: x + (barW - 8) / 2, y: height - 12, "text-anchor": "middle", "font-size": 11, fill: "#444" });
    label.textContent = payload.tokens[index];
    svg.appendChild(label);
  });
  const canvas = document.createElement("canvas");
  const cell = 36;
  canvas.width = payload.tokens.length * cell + 80;
  canvas.height = payload.tokens.length * cell + 36;
  canvas.style.cssText = "display:block;margin-top:8px;background:#fff;border:1px solid #eee;max-width:100%;";
  const ctx = canvas.getContext("2d");
  ctx.font = "12px sans-serif";
  ctx.fillStyle = "#222";
  ctx.fillText("完整注意力矩阵（行=query，列=key）", 8, 16);
  const peak = Math.max(...payload.weights.flat());
  payload.weights.forEach((weights, i) => {
    weights.forEach((value, j) => {
      ctx.fillStyle = sequential(value / peak);
      ctx.fillRect(70 + j * cell, 24 + i * cell, cell - 2, cell - 2);
    });
    ctx.fillStyle = "#444";
    ctx.fillText(payload.tokens[i], 4, 24 + i * cell + 20);
  });
  host.append(svg, canvas);
}

function paintQK(host, payload, state) {
  host.replaceChildren();
  const n = payload.tokens.length;
  const causal = !!state.causal;
  const canvas = document.createElement("canvas");
  const cell = 48;
  canvas.width = n * cell + 90;
  canvas.height = n * cell + 48;
  canvas.style.cssText = "background:#fff;border:1px solid #eee;max-width:100%;";
  const ctx = canvas.getContext("2d");
  ctx.font = "14px sans-serif";
  ctx.fillStyle = "#222";
  ctx.fillText(causal ? "因果 mask：只能看自己与过去" : "QKᵀ / √d_k（无 mask）", 8, 20);
  let peak = 1e-6;
  payload.scores.forEach((row) => row.forEach((value) => {
    peak = Math.max(peak, Math.abs(value));
  }));
  for (let i = 0; i < n; i += 1) {
    ctx.fillStyle = "#444";
    ctx.font = "12px sans-serif";
    ctx.fillText(payload.tokens[i], 4, 40 + i * cell + 24);
    for (let j = 0; j < n; j += 1) {
      const hidden = causal && j > i;
      ctx.fillStyle = hidden ? "#f4f4f4" : diverging(payload.scores[i][j] / (2 * peak) + 0.5);
      ctx.fillRect(70 + j * cell, 32 + i * cell, cell - 3, cell - 3);
      if (!hidden) {
        ctx.fillStyle = "#222";
        ctx.fillText(payload.scores[i][j].toFixed(1), 76 + j * cell, 56 + i * cell);
      }
    }
  }
  host.appendChild(canvas);
}

function gdLoss(x, y) {
  return (x - 1.2) ** 2 + 0.4 * (y + 0.8) ** 2 + 0.15 * Math.sin(3 * x) * Math.cos(2 * y);
}

function gdGrad(x, y) {
  return [
    2 * (x - 1.2) + 0.45 * Math.cos(3 * x) * Math.cos(2 * y),
    0.8 * (y + 0.8) - 0.3 * Math.sin(3 * x) * Math.sin(2 * y),
  ];
}

function paintDescent(host, payload, state, memory) {
  if (!memory.path) memory.path = [{ x: -1.8, y: 2 }];
  if (memory.action === "step" || memory.action === "play") {
    const last = memory.path[memory.path.length - 1];
    const [gx, gy] = gdGrad(last.x, last.y);
    memory.path.push({ x: last.x - state.lr * gx, y: last.y - state.lr * gy });
  }
  if (memory.action === "reset") memory.path = [{ x: -1.8, y: 2 }];
  memory.action = null;
  const canvas = document.createElement("canvas");
  canvas.style.cssText = "background:#fff;border:1px solid #eee;max-width:100%;";
  const ctx = canvas.getContext("2d");
  const grid = payload.grid;
  const zz = payload.zz;
  const n = grid.length;
  let zmin = Infinity;
  let zmax = -Infinity;
  zz.forEach((row) => row.forEach((value) => {
    zmin = Math.min(zmin, value);
    zmax = Math.max(zmax, value);
  }));
  const padL = 64;
  const padR = 16;
  const padT = 16;
  const padB = 46;
  const plot = 480;
  canvas.width = padL + plot + padR;
  canvas.height = padT + plot + padB;
  const xmin = -2.5;
  const xmax = 3.5;
  const toXY = (x, y) => [
    padL + ((x - xmin) / (xmax - xmin)) * plot,
    padT + ((xmax - y) / (xmax - xmin)) * plot,
  ];
  const cell = plot / n;
  ctx.save();
  ctx.beginPath();
  ctx.rect(padL, padT, plot, plot);
  ctx.clip();
  for (let i = 0; i < n; i += 1) {
    for (let j = 0; j < n; j += 1) {
      ctx.fillStyle = viridis((zz[i][j] - zmin) / (zmax - zmin + 1e-9));
      const [x, y] = toXY(grid[j], grid[i]);
      ctx.fillRect(x, y, cell + 0.5, cell + 0.5);
    }
  }
  ctx.restore();
  ctx.strokeStyle = "#222";
  ctx.lineWidth = 1;
  ctx.strokeRect(padL + 0.5, padT + 0.5, plot, plot);
  ctx.fillStyle = "#333";
  ctx.font = "12px sans-serif";
  ctx.textAlign = "center";
  for (const tick of [-2, -1, 0, 1, 2, 3]) {
    const [x] = toXY(tick, xmax);
    const [, y] = toXY(xmin, tick);
    ctx.beginPath();
    ctx.moveTo(x, padT + plot);
    ctx.lineTo(x, padT + plot + 6);
    ctx.moveTo(padL - 6, y);
    ctx.lineTo(padL, y);
    ctx.stroke();
    ctx.fillText(String(tick), x, padT + plot + 18);
    ctx.textAlign = "right";
    ctx.fillText(String(tick), padL - 8, y + 4);
    ctx.textAlign = "center";
  }
  ctx.fillText("参数 x", padL + plot / 2, canvas.height - 8);
  ctx.save();
  ctx.translate(16, padT + plot / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("参数 y", 0, 0);
  ctx.restore();
  ctx.strokeStyle = "#E45756";
  ctx.lineWidth = 2;
  ctx.beginPath();
  memory.path.forEach((point, index) => {
    const [x, y] = toXY(point.x, point.y);
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
  memory.path.forEach((point) => {
    const [x, y] = toXY(point.x, point.y);
    ctx.fillStyle = "#E45756";
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
  });
  const last = memory.path[memory.path.length - 1];
  host.replaceChildren(canvas);
  const note = document.createElement("div");
  note.style.cssText = "margin-top:6px;font:13px sans-serif;";
  note.textContent = `当前位置 (${last.x.toFixed(3)}, ${last.y.toFixed(3)})，loss = ${gdLoss(last.x, last.y).toFixed(4)}，步数 = ${memory.path.length - 1}`;
  host.appendChild(note);
}

function project(point, rotX, rotY) {
  const cy = Math.cos(rotY);
  const sy = Math.sin(rotY);
  const x1 = cy * point[0] + sy * point[2];
  const z1 = -sy * point[0] + cy * point[2];
  const cx = Math.cos(rotX);
  const sx = Math.sin(rotX);
  return [x1, cx * point[1] - sx * z1];
}

function paintEmbedding(host, payload, state, memory) {
  memory.rotX = memory.rotX ?? 0.5;
  memory.rotY = memory.rotY ?? -0.6;
  let canvas = memory.canvas;
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.width = 720;
    canvas.height = 480;
    canvas.style.cssText = "background:#fff;border:1px solid #eee;max-width:100%;cursor:grab;touch-action:none;";
    memory.canvas = canvas;
    host.replaceChildren(canvas);
    canvas.onpointerdown = (event) => {
      canvas.setPointerCapture(event.pointerId);
      memory.drag = { x: event.clientX, y: event.clientY };
    };
    canvas.onpointermove = (event) => {
      if (!memory.drag) return;
      memory.rotY += (event.clientX - memory.drag.x) * 0.01;
      memory.rotX += (event.clientY - memory.drag.y) * 0.01;
      memory.drag = { x: event.clientX, y: event.clientY };
      paintEmbedding(host, payload, state, memory);
    };
    canvas.onpointerup = () => {
      memory.drag = null;
    };
  }
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#222";
  ctx.font = "14px sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(memory.note || "拖动画布旋转。红箭头是 king − man + woman 的合向量。", 12, 22);
  const toScreen = (point) => {
    const [x, y] = project(point, memory.rotX, memory.rotY);
    return [360 + x * 220, 260 - y * 220];
  };
  const arrow = (from, to, color, label) => {
    const [x1, y1] = toScreen(from);
    const [x2, y2] = toScreen(to);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    const ang = Math.atan2(y2 - y1, x2 - x1);
    const ah = 9;
    ctx.beginPath();
    ctx.moveTo(x2, y2);
    ctx.lineTo(x2 - ah * Math.cos(ang - 0.45), y2 - ah * Math.sin(ang - 0.45));
    ctx.lineTo(x2 - ah * Math.cos(ang + 0.45), y2 - ah * Math.sin(ang + 0.45));
    ctx.closePath();
    ctx.fill();
    if (label) {
      ctx.font = "12px sans-serif";
      ctx.fillText(label, x2 + 6, y2 - 6);
    }
  };
  arrow([0, 0, 0], [1.1, 0, 0], "#E45756", "dim1");
  arrow([0, 0, 0], [0, 1.1, 0], "#54A24B", "dim2");
  arrow([0, 0, 0], [0, 0, 1.1], "#4C78A8", "dim3");
  const drawPoint = (point, color, text) => {
    const [cx, cy] = toScreen(point);
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(cx, cy, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#222";
    ctx.font = "13px sans-serif";
    ctx.textAlign = "left";
    ctx.fillText(text, cx + 8, cy - 8);
  };
  payload.points.forEach((point, index) => drawPoint(point, "#4C78A8", payload.labels[index]));
  if (memory.analogy) {
    arrow([0, 0, 0], memory.analogy, "#F58518", "合向量");
    drawPoint(memory.analogy, "#E45756", "king−man+woman");
  }
}

const painters = {
  neuron: paintNeuron,
  softmax: paintSoftmax,
  positional: paintPositional,
  attention: paintAttention,
  qk: paintQK,
  descent: paintDescent,
  embedding: paintEmbedding,
};

function render({ model, el }) {
  const spec = model.get("spec");
  const state = {};
  const memory = {};
  el.style.display = "block";
  const controls = document.createElement("div");
  const plot = document.createElement("div");
  el.replaceChildren(controls, plot);

  const paint = () => {
    const draw = painters[spec.kind];
    if (draw) draw(plot, spec.payload, state, memory);
  };

  const onInput = (name) => {
    if (spec.kind === "descent") {
      if (name === "play") {
        if (memory.timer) return;
        let left = 40;
        memory.timer = setInterval(() => {
          memory.action = "step";
          paint();
          left -= 1;
          if (left <= 0) {
            clearInterval(memory.timer);
            memory.timer = null;
          }
        }, 50);
        return;
      }
      if (name === "stop") {
        if (memory.timer) clearInterval(memory.timer);
        memory.timer = null;
        return;
      }
      if (name === "reset") {
        if (memory.timer) clearInterval(memory.timer);
        memory.timer = null;
        memory.action = "reset";
      }
      if (name === "step") memory.action = "step";
    }
    if (spec.kind === "embedding" && name === "analogy") {
      const words = Object.fromEntries(spec.payload.labels.map((label, index) => [label, spec.payload.points[index]]));
      const king = words.king;
      const man = words.man;
      const woman = words.woman;
      memory.analogy = king.map((value, index) => value - man[index] + woman[index]);
      let best = null;
      let bestDist = 1e9;
      for (const label of spec.payload.labels) {
        if (label === "king" || label === "man" || label === "woman") continue;
        const point = words[label];
        const dist = Math.hypot(
          memory.analogy[0] - point[0],
          memory.analogy[1] - point[1],
          memory.analogy[2] - point[2],
        );
        if (dist < bestDist) {
          bestDist = dist;
          best = label;
        }
      }
      memory.note = `类比结果：king − man + woman ≈ ${best}（距离 ${bestDist.toFixed(3)}）`;
    }
    if (spec.kind === "embedding" && name === "clear") {
      memory.analogy = null;
      memory.note = "已清除类比点。";
    }
    paint();
    if (memory.note) {
      let note = plot.querySelector("[data-note]");
      if (!note) {
        note = document.createElement("div");
        note.dataset.note = "1";
        note.style.cssText = "margin-top:6px;font:13px sans-serif;";
        plot.appendChild(note);
      }
      note.textContent = memory.note;
    }
  };

  mountControls(controls, spec.controls, state, onInput);
  paint();
}

export default { render };
