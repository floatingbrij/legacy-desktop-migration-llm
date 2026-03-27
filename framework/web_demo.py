"""
WEB DEMO: Visual Migration Framework Demo
==========================================
Flask-based web interface showing real-time migration progress.

Usage:
  cd c:\Organized\Research Migrate\framework
  python web_demo.py

Opens browser at http://localhost:5050
"""

import os
import sys
import json
import time
import threading
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template_string, jsonify, request
from parser import parse_designer_cs, parse_code_behind
from ir import winforms_to_ir, ir_to_json
from rules import apply_rules, CONTROL_RULES
from agents.analyzer import create_transformation_plan
from agents.translator import generate_xaml_page
from agents.refactoring import create_viewmodel
from agents.verification import verify_migration
from pipeline import MigrationPipeline

app = Flask(__name__)

FRAMEWORK_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_APPS_DIR = os.path.join(FRAMEWORK_DIR, "test_apps")

# Global state for experiment progress
experiment_state = {
    "running": False,
    "progress": [],
    "current_mode": "",
    "current_app": "",
    "done": False,
    "summary": {}
}

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WinForms to WinUI 3 Migration Framework</title>
<style>
  :root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
    --green: #3fb950; --red: #f85149; --yellow: #d29922;
    --purple: #bc8cff; --orange: #f0883e;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); }

  .header {
    background: linear-gradient(135deg, #1a1f35 0%, #0d1117 100%);
    border-bottom: 1px solid var(--border);
    padding: 24px 40px;
  }
  .header h1 { font-size: 22px; font-weight: 600; }
  .header h1 span { color: var(--accent); }
  .header p { color: var(--muted); font-size: 14px; margin-top: 4px; }

  .container { max-width: 1200px; margin: 0 auto; padding: 24px 40px; }

  .tabs {
    display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 24px;
  }
  .tab {
    padding: 10px 20px; cursor: pointer; color: var(--muted);
    border-bottom: 2px solid transparent; font-size: 14px; font-weight: 500;
    transition: all 0.2s;
  }
  .tab:hover { color: var(--text); }
  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }

  .panel { display: none; }
  .panel.active { display: block; }

  /* Single App Demo */
  .stage-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; margin-bottom: 16px; overflow: hidden;
  }
  .stage-header {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 20px; cursor: pointer; user-select: none;
  }
  .stage-header:hover { background: rgba(88,166,255,0.04); }
  .stage-num {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700;
    background: var(--border); color: var(--muted);
  }
  .stage-num.done { background: var(--green); color: #000; }
  .stage-num.active { background: var(--accent); color: #000; animation: pulse 1.5s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.6} }
  .stage-title { font-weight: 600; font-size: 15px; flex: 1; }
  .stage-time { color: var(--muted); font-size: 13px; font-family: monospace; }
  .stage-body { padding: 0 20px 16px 60px; }
  .stage-body.collapsed { display: none; }

  .stat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin: 10px 0; }
  .stat-box {
    background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 12px;
  }
  .stat-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
  .stat-value { font-size: 20px; font-weight: 700; margin-top: 4px; }
  .stat-value.green { color: var(--green); }
  .stat-value.yellow { color: var(--yellow); }
  .stat-value.red { color: var(--red); }

  .code-block {
    background: #0d1117; border: 1px solid var(--border); border-radius: 6px;
    padding: 12px 16px; font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 12px; line-height: 1.6; overflow-x: auto; white-space: pre;
    color: #c9d1d9; margin: 10px 0; max-height: 300px; overflow-y: auto;
  }
  .code-label { font-size: 12px; color: var(--muted); margin-bottom: 4px; font-weight: 600; }

  table.data-table {
    width: 100%; border-collapse: collapse; font-size: 13px; margin: 10px 0;
  }
  .data-table th, .data-table td {
    text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border);
  }
  .data-table th { color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; }
  .data-table tr:hover { background: rgba(88,166,255,0.04); }

  .badge {
    display: inline-block; padding: 2px 8px; border-radius: 10px;
    font-size: 11px; font-weight: 600;
  }
  .badge-green { background: rgba(63,185,80,0.15); color: var(--green); }
  .badge-yellow { background: rgba(210,153,34,0.15); color: var(--yellow); }
  .badge-red { background: rgba(248,81,73,0.15); color: var(--red); }

  /* Full Experiment */
  .btn {
    padding: 10px 24px; border-radius: 6px; font-size: 14px;
    font-weight: 600; cursor: pointer; border: none; transition: all 0.2s;
  }
  .btn-primary { background: var(--accent); color: #000; }
  .btn-primary:hover { background: #79c0ff; }
  .btn-primary:disabled { background: var(--border); color: var(--muted); cursor: not-allowed; }

  .progress-bar-bg {
    width: 100%; height: 8px; background: var(--border); border-radius: 4px; margin: 16px 0;
    overflow: hidden;
  }
  .progress-bar-fill {
    height: 100%; background: linear-gradient(90deg, var(--accent), var(--green));
    border-radius: 4px; transition: width 0.3s ease;
  }

  .mode-section { margin-bottom: 24px; }
  .mode-title {
    font-size: 14px; font-weight: 600; color: var(--yellow);
    margin-bottom: 8px; display: flex; align-items: center; gap: 8px;
  }
  .mode-title .indicator {
    width: 8px; height: 8px; border-radius: 50%; background: var(--border);
  }
  .mode-title .indicator.active { background: var(--yellow); animation: pulse 1s infinite; }
  .mode-title .indicator.done { background: var(--green); }

  .app-row {
    display: flex; align-items: center; gap: 12px; padding: 6px 0;
    font-size: 13px; font-family: monospace;
  }
  .app-name { width: 240px; color: var(--text); }
  .app-metric { width: 80px; text-align: right; }

  /* Summary cards */
  .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 20px 0; }
  .summary-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px;
    text-align: center;
  }
  .summary-card h3 { font-size: 13px; color: var(--muted); margin-bottom: 12px; text-transform: uppercase; }
  .summary-card .big-num { font-size: 36px; font-weight: 700; }
  .summary-card .sub { font-size: 12px; color: var(--muted); margin-top: 4px; }

  .app-select {
    background: var(--surface); color: var(--text); border: 1px solid var(--border);
    padding: 8px 12px; border-radius: 6px; font-size: 14px; margin-right: 12px;
    min-width: 250px;
  }
  .controls-row { display: flex; align-items: center; margin-bottom: 20px; gap: 12px; }

  .spinner { display: inline-block; width: 16px; height: 16px;
    border: 2px solid var(--border); border-top-color: var(--accent);
    border-radius: 50%; animation: spin 0.8s linear infinite; margin-left: 8px;
    vertical-align: middle;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .comparison-chart { margin: 20px 0; }
  .bar-row { display: flex; align-items: center; margin-bottom: 8px; }
  .bar-label { width: 120px; font-size: 13px; font-weight: 600; }
  .bar-track { flex: 1; height: 24px; background: var(--border); border-radius: 4px; overflow: hidden; position: relative; }
  .bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; display: flex; align-items: center;
    padding-left: 8px; font-size: 11px; font-weight: 700; color: #000; }
  .bar-fill.rule { background: var(--orange); }
  .bar-fill.single { background: var(--purple); }
  .bar-fill.hybrid { background: var(--green); }
</style>
</head>
<body>

<div class="header">
  <h1><span>WinForms &rarr; WinUI 3</span> Migration Framework</h1>
  <p>Brijesharun G, Dr. Hariprasad S &mdash; SRM Institute of Science and Technology</p>
</div>

<div class="container">
  <div class="tabs">
    <div class="tab active" onclick="switchTab('single')">Single App Demo</div>
    <div class="tab" onclick="switchTab('experiment')">Full Experiment (12 Apps &times; 3 Baselines)</div>
  </div>

  <!-- ====== SINGLE APP DEMO ====== -->
  <div id="panel-single" class="panel active">
    <div class="controls-row">
      <select id="app-select" class="app-select"></select>
      <button class="btn btn-primary" id="btn-run" onclick="runSingleDemo()">Run Migration</button>
    </div>
    <div id="stages-container"></div>
  </div>

  <!-- ====== FULL EXPERIMENT ====== -->
  <div id="panel-experiment" class="panel">
    <button class="btn btn-primary" id="btn-experiment" onclick="runExperiment()">Run Full Experiment</button>
    <div id="exp-progress" style="display:none">
      <div class="progress-bar-bg"><div class="progress-bar-fill" id="exp-bar" style="width:0%"></div></div>
      <div style="color:var(--muted);font-size:13px" id="exp-status">Starting...</div>
    </div>
    <div id="exp-results"></div>
  </div>
</div>

<script>
function switchTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  if (name === 'single') {
    document.querySelectorAll('.tab')[0].classList.add('active');
    document.getElementById('panel-single').classList.add('active');
  } else {
    document.querySelectorAll('.tab')[1].classList.add('active');
    document.getElementById('panel-experiment').classList.add('active');
  }
}

// Load app list
fetch('/api/apps').then(r=>r.json()).then(apps => {
  const sel = document.getElementById('app-select');
  apps.forEach(a => {
    const opt = document.createElement('option');
    opt.value = a.name;
    opt.textContent = a.name + ' (' + a.controls + ' controls, ' + a.events + ' events)';
    sel.appendChild(opt);
  });
});

function escapeHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function runSingleDemo() {
  const appName = document.getElementById('app-select').value;
  const btn = document.getElementById('btn-run');
  btn.disabled = true;
  btn.innerHTML = 'Running...<span class="spinner"></span>';
  document.getElementById('stages-container').innerHTML = '';

  fetch('/api/demo?app=' + encodeURIComponent(appName))
    .then(r => r.json())
    .then(data => {
      btn.disabled = false;
      btn.textContent = 'Run Migration';
      renderStages(data);
    })
    .catch(err => {
      btn.disabled = false;
      btn.textContent = 'Run Migration';
      document.getElementById('stages-container').innerHTML =
        '<div style="color:var(--red)">Error: ' + err.message + '</div>';
    });
}

function renderStages(data) {
  const container = document.getElementById('stages-container');
  let html = '';

  // Stage 1: Static Analysis
  const s1 = data.stage1;
  html += stageCard(1, 'Static Analysis (Roslyn Parser)', s1.time_ms, `
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-label">Class</div><div class="stat-value">${escapeHtml(s1.class_name)}</div></div>
      <div class="stat-box"><div class="stat-label">Controls Found</div><div class="stat-value green">${s1.controls_count}</div></div>
      <div class="stat-box"><div class="stat-label">Event Handlers</div><div class="stat-value">${s1.handlers_count}</div></div>
      <div class="stat-box"><div class="stat-label">Parse Time</div><div class="stat-value">${s1.time_ms.toFixed(1)} ms</div></div>
    </div>
    <table class="data-table">
      <thead><tr><th>Control Type</th><th>Name</th><th>Events</th></tr></thead>
      <tbody>${s1.controls.map(c => `<tr><td>${escapeHtml(c.type)}</td><td>${escapeHtml(c.name)}</td><td>${escapeHtml(c.events)}</td></tr>`).join('')}</tbody>
    </table>
  `);

  // Stage 2: IR
  const s2 = data.stage2;
  html += stageCard(2, 'Intermediate Representation', s2.time_ms, `
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-label">Form ID</div><div class="stat-value" style="font-size:14px">${escapeHtml(s2.form_id)}</div></div>
      <div class="stat-box"><div class="stat-label">Controls in IR</div><div class="stat-value green">${s2.controls_count}</div></div>
      <div class="stat-box"><div class="stat-label">Complexity</div><div class="stat-value yellow">${escapeHtml(s2.complexity)}</div></div>
    </div>
  `);

  // Stage 3: Rules
  const s3 = data.stage3;
  html += stageCard(3, 'Rule-Based Transformation', s3.time_ms, `
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-label">Rules in Engine</div><div class="stat-value">${s3.total_rules}</div></div>
      <div class="stat-box"><div class="stat-label">Transformations</div><div class="stat-value green">${s3.transformations_count}</div></div>
    </div>
    <table class="data-table">
      <thead><tr><th>Original</th><th>WinUI 3 Tag</th><th>Confidence</th></tr></thead>
      <tbody>${s3.transformations.map(t => `<tr><td>${escapeHtml(t.original)}</td><td>${escapeHtml(t.target)}</td><td><span class="badge ${t.confidence >= 0.9 ? 'badge-green' : 'badge-yellow'}">${(t.confidence*100).toFixed(0)}%</span></td></tr>`).join('')}</tbody>
    </table>
  `);

  // Stage 4: Agents
  const s4 = data.stage4;
  html += stageCard(4, 'Multi-Agent LLM Pipeline', s4.time_ms, `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
      <div>
        <div class="code-label">Agent 1: Analyzer</div>
        <div class="stat-grid" style="grid-template-columns:1fr 1fr">
          <div class="stat-box"><div class="stat-label">Patterns Detected</div><div class="stat-value">${s4.analyzer.patterns_count}</div></div>
          <div class="stat-box"><div class="stat-label">MVVM Candidates</div><div class="stat-value">${s4.analyzer.mvvm_count}</div></div>
        </div>
        ${s4.analyzer.patterns.length ? '<div style="margin-top:6px;font-size:12px;color:var(--muted)">' + s4.analyzer.patterns.map(p=>'&bull; '+escapeHtml(p)).join('<br>') + '</div>' : ''}
      </div>
      <div>
        <div class="code-label">Agent 2: Translator</div>
        <div class="stat-grid" style="grid-template-columns:1fr 1fr">
          <div class="stat-box"><div class="stat-label">Controls Generated</div><div class="stat-value green">${s4.translator.controls_generated}</div></div>
          <div class="stat-box"><div class="stat-label">Controls Skipped</div><div class="stat-value ${s4.translator.controls_skipped > 0 ? 'red' : ''}">${s4.translator.controls_skipped}</div></div>
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px">
      <div>
        <div class="code-label">Agent 3: Refactoring (MVVM)</div>
        <div class="stat-grid" style="grid-template-columns:1fr 1fr">
          <div class="stat-box"><div class="stat-label">Events Converted</div><div class="stat-value">${s4.refactoring.events_converted}</div></div>
          <div class="stat-box"><div class="stat-label">Properties</div><div class="stat-value">${s4.refactoring.properties_converted}</div></div>
        </div>
      </div>
      <div>
        <div class="code-label">Agent 4: Verification</div>
        <div class="stat-grid" style="grid-template-columns:1fr 1fr">
          <div class="stat-box"><div class="stat-label">Issues</div><div class="stat-value ${s4.verification.total_issues > 0 ? 'yellow' : 'green'}">${s4.verification.total_issues}</div></div>
          <div class="stat-box"><div class="stat-label">Fixes Applied</div><div class="stat-value green">${s4.verification.fixes_applied}</div></div>
        </div>
        <div class="stat-grid" style="grid-template-columns:1fr">
          <div class="stat-box"><div class="stat-label">Estimated Compilability</div><div class="stat-value ${s4.verification.compilability >= 80 ? 'green' : s4.verification.compilability >= 60 ? 'yellow' : 'red'}">${s4.verification.compilability.toFixed(1)}%</div></div>
        </div>
      </div>
    </div>
    <div style="margin-top:16px">
      <div class="code-label">Generated XAML</div>
      <div class="code-block">${escapeHtml(s4.xaml_preview)}</div>
    </div>
    ${s4.viewmodel_preview ? `<div style="margin-top:12px"><div class="code-label">Generated ViewModel</div><div class="code-block">${escapeHtml(s4.viewmodel_preview)}</div></div>` : ''}
  `);

  // Stage 5: Summary
  const s5 = data.stage5;
  html += stageCard(5, 'Output Summary', s5.total_time_ms, `
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-label">CSR</div><div class="stat-value ${s5.csr >= 80 ? 'green' : s5.csr >= 60 ? 'yellow' : 'red'}">${s5.csr.toFixed(1)}%</div></div>
      <div class="stat-box"><div class="stat-label">Migration Completeness</div><div class="stat-value ${s5.mc >= 90 ? 'green' : 'yellow'}">${s5.mc.toFixed(1)}%</div></div>
      <div class="stat-box"><div class="stat-label">UI Parity Score</div><div class="stat-value green">${s5.ups.toFixed(1)}%</div></div>
      <div class="stat-box"><div class="stat-label">Error Density</div><div class="stat-value ${s5.ed < 1 ? 'green' : 'yellow'}">${s5.ed.toFixed(2)}</div></div>
    </div>
    <table class="data-table" style="margin-top:12px">
      <thead><tr><th>Generated File</th><th>Lines</th></tr></thead>
      <tbody>
        ${s5.files.map(f => `<tr><td>${escapeHtml(f.name)}</td><td>${f.lines}</td></tr>`).join('')}
      </tbody>
    </table>
  `);

  container.innerHTML = html;
}

function stageCard(num, title, timeMs, body) {
  return `
    <div class="stage-card">
      <div class="stage-header" onclick="this.nextElementSibling.classList.toggle('collapsed')">
        <div class="stage-num done">${num}</div>
        <div class="stage-title">${title}</div>
        <div class="stage-time">${timeMs.toFixed(1)} ms</div>
      </div>
      <div class="stage-body">${body}</div>
    </div>`;
}

// ====== FULL EXPERIMENT ======
let expPoll = null;

function runExperiment() {
  const btn = document.getElementById('btn-experiment');
  btn.disabled = true;
  btn.innerHTML = 'Running...<span class="spinner"></span>';
  document.getElementById('exp-progress').style.display = 'block';
  document.getElementById('exp-results').innerHTML = '';

  fetch('/api/experiment', {method:'POST'}).then(r=>r.json());

  expPoll = setInterval(() => {
    fetch('/api/experiment/status').then(r=>r.json()).then(state => {
      renderExperimentProgress(state);
      if (state.done) {
        clearInterval(expPoll);
        btn.disabled = false;
        btn.textContent = 'Run Full Experiment';
        renderExperimentSummary(state);
      }
    });
  }, 500);
}

function renderExperimentProgress(state) {
  const total = 36; // 12 apps x 3 modes
  const completed = state.progress.length;
  const pct = (completed / total * 100).toFixed(0);
  document.getElementById('exp-bar').style.width = pct + '%';
  document.getElementById('exp-status').textContent =
    state.running ? `Running ${state.current_mode.toUpperCase()} — ${state.current_app} (${completed}/${total})` :
    state.done ? `Complete! ${completed} migrations finished.` : 'Waiting...';

  // Render per-mode results
  let html = '';
  const modes = ['rule_only', 'single_agent', 'hybrid'];
  const modeLabels = {'rule_only': 'Rule-Only', 'single_agent': 'Single-Agent', 'hybrid': 'Hybrid (Ours)'};
  const modeColors = {'rule_only': 'var(--orange)', 'single_agent': 'var(--purple)', 'hybrid': 'var(--green)'};

  for (const mode of modes) {
    const items = state.progress.filter(p => p.mode === mode);
    if (items.length === 0) continue;
    const isCurrent = state.current_mode === mode && state.running;
    const isDone = items.length === 12;

    html += `<div class="mode-section">
      <div class="mode-title">
        <div class="indicator ${isCurrent ? 'active' : isDone ? 'done' : ''}"></div>
        <span style="color:${modeColors[mode]}">${modeLabels[mode]}</span>
        <span style="color:var(--muted);font-size:12px">(${items.length}/12)</span>
      </div>`;

    for (const item of items) {
      const csrColor = item.csr >= 80 ? 'var(--green)' : item.csr >= 60 ? 'var(--yellow)' : 'var(--red)';
      html += `<div class="app-row">
        <span class="app-name">${escapeHtml(item.app)}</span>
        <span class="app-metric" style="color:${csrColor}">CSR ${item.csr.toFixed(1)}%</span>
        <span class="app-metric" style="color:var(--muted)">MC ${item.mc.toFixed(1)}%</span>
        <span class="app-metric" style="color:var(--muted)">ED ${item.ed.toFixed(2)}</span>
        ${item.error ? '<span class="badge badge-red">ERROR</span>' : ''}
      </div>`;
    }
    html += '</div>';
  }
  document.getElementById('exp-results').innerHTML = html;
}

function renderExperimentSummary(state) {
  if (!state.summary || !state.summary.rule_only) return;
  const s = state.summary;
  const modes = ['rule_only', 'single_agent', 'hybrid'];
  const labels = {'rule_only': 'Rule-Only', 'single_agent': 'Single-Agent', 'hybrid': 'Hybrid'};

  let html = '<h2 style="margin:24px 0 12px;font-size:18px">Experiment Summary</h2>';
  html += '<div class="summary-grid">';
  for (const mode of modes) {
    const d = s[mode];
    const color = mode === 'hybrid' ? 'var(--green)' : mode === 'single_agent' ? 'var(--purple)' : 'var(--orange)';
    html += `<div class="summary-card">
      <h3 style="color:${color}">${labels[mode]}</h3>
      <div class="big-num" style="color:${color}">${d.avg_csr.toFixed(1)}%</div>
      <div class="sub">Avg CSR</div>
      <div style="margin-top:12px;font-size:13px;color:var(--muted)">
        MC: ${d.avg_mc.toFixed(1)}% &nbsp; ED: ${d.avg_ed.toFixed(2)}
      </div>
    </div>`;
  }
  html += '</div>';

  // Bar chart comparison
  html += '<div class="comparison-chart"><h3 style="margin-bottom:12px;font-size:15px">Compilation Success Rate Comparison</h3>';
  for (const mode of modes) {
    const d = s[mode];
    const cls = mode === 'hybrid' ? 'hybrid' : mode === 'single_agent' ? 'single' : 'rule';
    html += `<div class="bar-row">
      <div class="bar-label">${labels[mode]}</div>
      <div class="bar-track"><div class="bar-fill ${cls}" style="width:${d.avg_csr}%">${d.avg_csr.toFixed(1)}%</div></div>
    </div>`;
  }
  html += '</div>';

  document.getElementById('exp-results').innerHTML += html;
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/apps")
def api_apps():
    """List available test apps with metadata."""
    apps = []
    for app_name in sorted(os.listdir(TEST_APPS_DIR)):
        app_path = os.path.join(TEST_APPS_DIR, app_name)
        if not os.path.isdir(app_path):
            continue
        for f in os.listdir(app_path):
            if f.endswith(".Designer.cs"):
                designer = os.path.join(app_path, f)
                form = parse_designer_cs(designer)
                cb_path = designer.replace(".Designer.cs", ".cs")
                handlers = parse_code_behind(cb_path) if os.path.exists(cb_path) else {}
                apps.append({
                    "name": app_name,
                    "designer": f,
                    "controls": len(form.controls),
                    "events": len(handlers),
                })
                break
    return jsonify(apps)


@app.route("/api/demo")
def api_demo():
    """Run single-app demo with stage-by-stage results."""
    app_name = request.args.get("app", "small_01_calculator")
    app_path = os.path.join(TEST_APPS_DIR, app_name)

    designer = None
    for f in os.listdir(app_path):
        if f.endswith(".Designer.cs"):
            designer = os.path.join(app_path, f)
            break
    if not designer:
        return jsonify({"error": "No .Designer.cs found"}), 404

    codebehind = designer.replace(".Designer.cs", ".cs")

    # Stage 1
    t0 = time.perf_counter()
    form = parse_designer_cs(designer)
    handlers = parse_code_behind(codebehind) if os.path.exists(codebehind) else {}
    form.event_handlers = handlers
    for ctrl in form.controls:
        for evt in ctrl.events:
            if evt.handler_name in handlers:
                evt.handler_body = handlers[evt.handler_name]
    t1 = time.perf_counter()

    stage1 = {
        "class_name": f"{form.namespace}.{form.class_name}",
        "controls_count": len(form.controls),
        "handlers_count": len(handlers),
        "time_ms": (t1 - t0) * 1000,
        "controls": [
            {
                "type": c.control_type,
                "name": c.name,
                "events": ", ".join(e.handler_name for e in c.events) if c.events else "none",
            }
            for c in form.controls
        ],
    }

    # Stage 2
    t2 = time.perf_counter()
    ir_form = winforms_to_ir(form)
    ir_json_str = ir_to_json(ir_form)
    ir_dict = json.loads(ir_json_str)
    t3 = time.perf_counter()

    stage2 = {
        "form_id": ir_dict.get("id", ""),
        "controls_count": len(ir_dict.get("controls", [])),
        "complexity": ir_dict.get("complexity_tier", "N/A"),
        "time_ms": (t3 - t2) * 1000,
    }

    # Stage 3
    t4 = time.perf_counter()
    rule_results = apply_rules(ir_dict)
    t5 = time.perf_counter()

    stage3 = {
        "total_rules": len(CONTROL_RULES),
        "transformations_count": len(rule_results.get("transformations", [])),
        "time_ms": (t5 - t4) * 1000,
        "transformations": [
            {
                "original": tr.get("original_type", ""),
                "target": tr.get("winui_tag", ""),
                "confidence": tr.get("confidence", 0),
            }
            for tr in rule_results.get("transformations", [])
        ],
    }

    # Stage 4
    t6 = time.perf_counter()
    plan = create_transformation_plan(ir_dict, rule_results)
    xaml_output = generate_xaml_page(ir_dict, rule_results, plan, migrate_handlers=True)

    mvvm_result = None
    if plan.mvvm_candidates:
        mvvm_result = create_viewmodel(
            ir_dict.get("id", ""),
            ir_dict.get("class_name", "MainForm"),
            ir_dict.get("namespace", "MigratedApp"),
            plan.mvvm_candidates,
            ir_dict,
        )

    vm_code = mvvm_result.viewmodel.code if mvvm_result and mvvm_result.viewmodel else ""
    verification = verify_migration(
        xaml_output.xaml_content, xaml_output.code_behind, vm_code, apply_fixes=True
    )
    t7 = time.perf_counter()

    stage4 = {
        "time_ms": (t7 - t6) * 1000,
        "analyzer": {
            "patterns_count": len(plan.detected_patterns),
            "mvvm_count": len(plan.mvvm_candidates),
            "patterns": plan.detected_patterns[:6],
        },
        "translator": {
            "controls_generated": xaml_output.controls_generated,
            "controls_skipped": xaml_output.controls_skipped,
            "xaml_lines": len(xaml_output.xaml_content.splitlines()),
            "cb_lines": len(xaml_output.code_behind.splitlines()),
        },
        "refactoring": {
            "events_converted": mvvm_result.events_converted if mvvm_result else 0,
            "properties_converted": mvvm_result.properties_converted if mvvm_result else 0,
            "viewmodel_name": mvvm_result.viewmodel.class_name if mvvm_result and mvvm_result.viewmodel else "N/A",
        },
        "verification": {
            "valid": verification.is_valid,
            "total_issues": verification.total_issues,
            "errors": verification.errors,
            "warnings": verification.warnings,
            "fixes_applied": verification.fixes_applied,
            "compilability": verification.estimated_compilability,
        },
        "xaml_preview": "\n".join(xaml_output.xaml_content.splitlines()[:30]),
        "viewmodel_preview": "\n".join(vm_code.splitlines()[:25]) if vm_code else "",
    }

    # Stage 5: compute metrics
    timings = {
        "parse": stage1["time_ms"],
        "ir": stage2["time_ms"],
        "rules": stage3["time_ms"],
        "agents": stage4["time_ms"],
        "transform": stage3["time_ms"] + stage4["time_ms"],
        "generate": stage4["time_ms"],
        "verify": stage4["time_ms"] * 0.3,
        "output": 0,
        "total": (t7 - t0) * 1000,
    }
    from metrics import compute_metrics

    metrics = compute_metrics(
        form_id=ir_dict.get("id", ""),
        ir_form=ir_dict,
        rule_results=rule_results,
        xaml_output=xaml_output,
        verification=verification,
        mvvm_result=mvvm_result,
        timings=timings,
        mode="hybrid",
    )

    files = [
        {"name": form.class_name + ".xaml", "lines": len(xaml_output.xaml_content.splitlines())},
        {"name": form.class_name + ".xaml.cs", "lines": len(xaml_output.code_behind.splitlines())},
    ]
    if vm_code:
        files.append({"name": "ViewModel.cs", "lines": len(vm_code.splitlines())})

    stage5 = {
        "total_time_ms": timings["total"],
        "csr": metrics.csr,
        "mc": metrics.mc,
        "ups": metrics.ups,
        "ed": metrics.ed,
        "files": files,
    }

    return jsonify({"stage1": stage1, "stage2": stage2, "stage3": stage3, "stage4": stage4, "stage5": stage5})


@app.route("/api/experiment", methods=["POST"])
def api_experiment_start():
    """Start full experiment in background thread."""
    if experiment_state["running"]:
        return jsonify({"status": "already_running"})

    experiment_state["running"] = True
    experiment_state["progress"] = []
    experiment_state["done"] = False
    experiment_state["summary"] = {}
    experiment_state["current_mode"] = ""
    experiment_state["current_app"] = ""

    def run():
        apps = []
        for app_name in sorted(os.listdir(TEST_APPS_DIR)):
            app_path = os.path.join(TEST_APPS_DIR, app_name)
            if not os.path.isdir(app_path):
                continue
            for f in os.listdir(app_path):
                if f.endswith(".Designer.cs"):
                    designer = os.path.join(app_path, f)
                    cb = designer.replace(".Designer.cs", ".cs")
                    apps.append({"name": app_name, "designer": designer,
                                 "code_behind": cb if os.path.exists(cb) else None})
                    break

        output_dir = os.path.join(FRAMEWORK_DIR, "demo_output")
        mode_results = {}

        for mode in ["rule_only", "single_agent", "hybrid"]:
            experiment_state["current_mode"] = mode
            mode_output = os.path.join(output_dir, mode)
            pipeline = MigrationPipeline(output_dir=mode_output, mode=mode)
            mode_results[mode] = []

            for a in apps:
                experiment_state["current_app"] = a["name"]
                try:
                    m = pipeline.migrate_file(a["designer"], a.get("code_behind"))
                    entry = {"app": a["name"], "mode": mode, "csr": m.csr, "mc": m.mc, "ed": m.ed, "error": False}
                except Exception as e:
                    entry = {"app": a["name"], "mode": mode, "csr": 0, "mc": 0, "ed": 0, "error": str(e)}
                experiment_state["progress"].append(entry)
                mode_results[mode].append(entry)

        # Compute summary
        summary = {}
        for mode, items in mode_results.items():
            valid = [i for i in items if not i["error"]]
            if valid:
                summary[mode] = {
                    "avg_csr": sum(i["csr"] for i in valid) / len(valid),
                    "avg_mc": sum(i["mc"] for i in valid) / len(valid),
                    "avg_ed": sum(i["ed"] for i in valid) / len(valid),
                    "count": len(valid),
                }
            else:
                summary[mode] = {"avg_csr": 0, "avg_mc": 0, "avg_ed": 0, "count": 0}

        experiment_state["summary"] = summary
        experiment_state["running"] = False
        experiment_state["done"] = True

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"status": "started"})


@app.route("/api/experiment/status")
def api_experiment_status():
    return jsonify(experiment_state)


if __name__ == "__main__":
    import webbrowser
    port = 5050
    print(f"\n  WinForms -> WinUI 3 Migration Framework - Web Demo")
    print(f"  Opening http://localhost:{port}\n")
    webbrowser.open(f"http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
