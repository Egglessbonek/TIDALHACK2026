<script>
  import { onMount } from 'svelte';
  import rough from 'roughjs/bundled/rough.esm.js';
  
  // City stats (read-only displays)
  let economy = 65;
  let health = 72;
  let education = 58;
  let crime = 34; // Lower is better
  let environment = 81;
  let population = 12500;
  let budget = 45000;
  
  // Buildings (read-only)
  let buildings = {
    hospitals: 1,
    schools: 3,
    parks: 5,
    factories: 4
  };
  
  // Infrastructure (modifiable - only transportation/utility infrastructure)
  let infrastructure = {
    highways: 2,
    bridges: 1,
    tunnels: 0,
    roads: 5,
    railroads: 1
  };
  
  // History tracking
  /** @type {Array<{timestamp: number, action: string, effect: string}>} */
  let history = [
    { timestamp: Date.now() - 3600000, action: "Built Highway #2", effect: "Economy +5%, Traffic -10%" },
    { timestamp: Date.now() - 7200000, action: "Built Bridge #1", effect: "Connectivity +15%" },
    { timestamp: Date.now() - 10800000, action: "Added 3 Roads", effect: "Accessibility +8%" }
  ];
  
  // SVG canvases for rough.js
  /** @type {SVGSVGElement | undefined} */
  let economyCanvas;
  /** @type {SVGSVGElement | undefined} */
  let healthCanvas;
  /** @type {SVGSVGElement | undefined} */
  let educationCanvas;
  /** @type {SVGSVGElement | undefined} */
  let crimeCanvas;
  /** @type {SVGSVGElement | undefined} */
  let environmentCanvas;
  
  /**
   * @param {keyof infrastructure} type
   * @param {number} delta
   */
  function adjustInfrastructure(type, delta) {
    if (infrastructure[type] + delta >= 0) {
      const oldValue = infrastructure[type];
      infrastructure[type] += delta;
      budget -= delta * 5000;
      
      // Add to history
      const infrastructureNames = {
        highways: 'Highway',
        bridges: 'Bridge',
        tunnels: 'Tunnel',
        roads: 'Road',
        railroads: 'Railroad'
      };
      
      const action = delta > 0 
        ? `Built ${infrastructureNames[type]} #${infrastructure[type]}`
        : `Removed ${infrastructureNames[type]} #${oldValue}`;
      
      // Calculate effect on stats (simplified)
      let effect = '';
      if (type === 'highways') {
        effect = delta > 0 ? 'Economy +5%, Traffic -8%' : 'Economy -3%, Traffic +5%';
        economy += delta * 5;
      } else if (type === 'bridges') {
        effect = delta > 0 ? 'Connectivity +10%' : 'Connectivity -10%';
      } else if (type === 'tunnels') {
        effect = delta > 0 ? 'Traffic -12%, Crime +2%' : 'Traffic +8%, Crime -1%';
        crime += delta * 2;
      } else if (type === 'roads') {
        effect = delta > 0 ? 'Accessibility +3%' : 'Accessibility -3%';
      } else if (type === 'railroads') {
        effect = delta > 0 ? 'Environment +8%, Economy +3%' : 'Environment -5%, Economy -2%';
        environment += delta * 8;
        economy += delta * 3;
      }
      
      // Clamp stats to 0-100
      economy = Math.max(0, Math.min(100, economy));
      crime = Math.max(0, Math.min(100, crime));
      environment = Math.max(0, Math.min(100, environment));
      
      history = [{ timestamp: Date.now(), action, effect }, ...history].slice(0, 10);
    }
  }
  
  /**

   * @param {SVGSVGElement | undefined} canvas
   * @param {number} percentage
   * @param {string} color
   */
  function drawHandDrawnBar(canvas, percentage, color) {
    if (!canvas) return;
    const rc = rough.svg(canvas);
    canvas.innerHTML = '';
    
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    
    // Draw background container
    const bg = rc.rectangle(0, 0, width, height, {
      fill: 'rgba(0, 0, 0, 0.3)',
      fillStyle: 'solid',
      stroke: '#fff',
      strokeWidth: 2,
      roughness: 2.5,
      bowing: 1
    });
    canvas.appendChild(bg);
    
    // Draw filled portion
    const barWidth = (width - 4) * (percentage / 100);
    if (barWidth > 2) {
      const bar = rc.rectangle(2, 2, barWidth, height - 4, {
        fill: color,
        fillStyle: 'zigzag',
        stroke: color,
        strokeWidth: 1,
        roughness: 2,
        bowing: 0.5,
        fillWeight: 3
      });
      canvas.appendChild(bar);
    }
  }
  
  onMount(() => {
    drawHandDrawnBar(economyCanvas, economy, '#4CAF50');
    drawHandDrawnBar(healthCanvas, health, '#f44336');
    drawHandDrawnBar(educationCanvas, education, '#2196F3');
    drawHandDrawnBar(crimeCanvas, crime, '#9C27B0');
    drawHandDrawnBar(environmentCanvas, environment, '#009688');
  });
  
  $: {
    if (economyCanvas) drawHandDrawnBar(economyCanvas, economy, '#4CAF50');
    if (healthCanvas) drawHandDrawnBar(healthCanvas, health, '#f44336');
    if (educationCanvas) drawHandDrawnBar(educationCanvas, education, '#2196F3');
    if (crimeCanvas) drawHandDrawnBar(crimeCanvas, crime, '#9C27B0');
    if (environmentCanvas) drawHandDrawnBar(environmentCanvas, environment, '#009688');
  }
</script>

<style>
  .dashboard-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 1200px;
    height: 85%;
    z-index: 10;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 20px;
    padding: 20px;
    pointer-events: auto;
    box-sizing: border-box;
  }

  .dashboard-container * {
    box-sizing: border-box;
  }

  @media (max-width: 768px) {
    .dashboard-container {
      grid-template-columns: 1fr;
      grid-template-rows: auto;
      height: 90%;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }
  }

  .dashboard-title {
    grid-column: 1 / -1;
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 36px;
    color: #2c3e50;
    text-align: center;
    margin: 0;
    padding-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 3px;
    transform: rotate(-1deg);
    filter: drop-shadow(3px 3px 0 rgba(255, 255, 255, 0.5));
  }

  .stats-panel {
    background: rgba(255, 255, 255, 0.85);
    border: 4px solid #2c3e50;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.2);
    transform: rotate(-0.5deg);
  }

  .stats-panel:nth-child(even) {
    transform: rotate(0.5deg);
  }

  .panel-title {
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 18px;
    color: #2c3e50;
    margin: 0 0 15px 0;
    padding-bottom: 8px;
    border-bottom: 3px solid #2c3e50;
    text-transform: uppercase;
  }

  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 12px;
    color: #2c3e50;
  }

  .stat-label {
    flex: 1;
    font-weight: bold;
  }

  .stat-value {
    font-weight: bold;
    margin-left: 10px;
    font-size: 14px;
  }

  .stat-value.negative {
    color: #f44336;
  }

  .stat-bar-container {
    flex: 2;
    height: 20px;
    margin-left: 10px;
    position: relative;
  }

  .stat-bar {
    width: 100%;
    height: 100%;
  }

  .infrastructure-panel {
    grid-column: 1 / -1;
  }

  .infrastructure-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }

  .infrastructure-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.6);
    padding: 10px 15px;
    border-radius: 8px;
    border: 3px solid #2c3e50;
    box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.15);
  }

  .infrastructure-label {
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 13px;
    color: #2c3e50;
    flex: 1;
    font-weight: bold;
  }

  .infrastructure-controls {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .infra-button {
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 18px;
    background: #fff;
    border: 3px solid #2c3e50;
    color: #2c3e50;
    width: 32px;
    height: 32px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.2);
    font-weight: bold;
  }

  .infra-button:hover {
    background: #f0f0f0;
    transform: translate(-1px, -1px);
    box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.2);
  }

  .infra-button:active {
    transform: translate(1px, 1px);
    box-shadow: 1px 1px 0 rgba(0, 0, 0, 0.2);
  }

  .infra-count {
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 16px;
    color: #2c3e50;
    min-width: 25px;
    text-align: center;
    font-weight: bold;
  }

  .history-panel {
    grid-column: 1 / -1;
    max-height: 200px;
  }

  .history-list {
    max-height: 150px;
    overflow-y: auto;
    padding-right: 5px;
  }

  .history-item {
    background: rgba(255, 255, 255, 0.5);
    padding: 8px 12px;
    margin-bottom: 8px;
    border-radius: 6px;
    border: 2px solid #2c3e50;
    font-family: 'Permanent Marker', 'Comic Sans MS', cursive, sans-serif;
    font-size: 10px;
    color: #2c3e50;
  }

  .history-action {
    font-weight: bold;
    margin-bottom: 3px;
  }

  .history-effect {
    color: #555;
    font-size: 9px;
  }

  .history-time {
    color: #888;
    font-size: 8px;
    margin-top: 2px;
  }
</style>

<div class="dashboard-container">
  <h1 class="dashboard-title">CITY DASHBOARD</h1>
  
  <!-- City Stats Panel -->
  <div class="stats-panel">
    <h2 class="panel-title">City Stats</h2>
    
    <div class="stat-row">
      <span class="stat-label">Economy</span>
      <div class="stat-bar-container">
        <svg bind:this={economyCanvas} class="stat-bar"></svg>
      </div>
      <span class="stat-value">{economy}%</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Health</span>
      <div class="stat-bar-container">
        <svg bind:this={healthCanvas} class="stat-bar"></svg>
      </div>
      <span class="stat-value">{health}%</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Education</span>
      <div class="stat-bar-container">
        <svg bind:this={educationCanvas} class="stat-bar"></svg>
      </div>
      <span class="stat-value">{education}%</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Crime</span>
      <div class="stat-bar-container">
        <svg bind:this={crimeCanvas} class="stat-bar"></svg>
      </div>
      <span class="stat-value">{crime}%</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Environment</span>
      <div class="stat-bar-container">
        <svg bind:this={environmentCanvas} class="stat-bar"></svg>
      </div>
      <span class="stat-value">{environment}%</span>
    </div>
  </div>
  
  <!-- Population & Budget Panel -->
  <div class="stats-panel">
    <h2 class="panel-title">Overview</h2>
    
    <div class="stat-row">
      <span class="stat-label">Population</span>
      <span class="stat-value">{population.toLocaleString()}</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Budget</span>
      <span class="stat-value" class:negative={budget < 0}>${Math.abs(budget).toLocaleString()}</span>
    </div>
    
    <h2 class="panel-title" style="margin-top: 15px;">Buildings</h2>
    
    <div class="stat-row">
      <span class="stat-label">Hospitals</span>
      <span class="stat-value">{buildings.hospitals}</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Schools</span>
      <span class="stat-value">{buildings.schools}</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Parks</span>
      <span class="stat-value">{buildings.parks}</span>
    </div>
    
    <div class="stat-row">
      <span class="stat-label">Factories</span>
      <span class="stat-value">{buildings.factories}</span>
    </div>
  </div>
  
  <!-- Infrastructure Panel -->
  <div class="stats-panel infrastructure-panel">
    <h2 class="panel-title">Infrastructure</h2>
    
    <div class="infrastructure-grid">
      <div class="infrastructure-item">
        <span class="infrastructure-label">Highways</span>
        <div class="infrastructure-controls">
          <button class="infra-button" on:click={() => adjustInfrastructure('highways', -1)}>-</button>
          <span class="infra-count">{infrastructure.highways}</span>
          <button class="infra-button" on:click={() => adjustInfrastructure('highways', 1)}>+</button>
        </div>
      </div>
      
      <div class="infrastructure-item">
        <span class="infrastructure-label">Bridges</span>
        <div class="infrastructure-controls">
          <button class="infra-button" on:click={() => adjustInfrastructure('bridges', -1)}>-</button>
          <span class="infra-count">{infrastructure.bridges}</span>
          <button class="infra-button" on:click={() => adjustInfrastructure('bridges', 1)}>+</button>
        </div>
      </div>
      
      <div class="infrastructure-item">
        <span class="infrastructure-label">Tunnels</span>
        <div class="infrastructure-controls">
          <button class="infra-button" on:click={() => adjustInfrastructure('tunnels', -1)}>-</button>
          <span class="infra-count">{infrastructure.tunnels}</span>
          <button class="infra-button" on:click={() => adjustInfrastructure('tunnels', 1)}>+</button>
        </div>
      </div>
      
      <div class="infrastructure-item">
        <span class="infrastructure-label">Roads</span>
        <div class="infrastructure-controls">
          <button class="infra-button" on:click={() => adjustInfrastructure('roads', -1)}>-</button>
          <span class="infra-count">{infrastructure.roads}</span>
          <button class="infra-button" on:click={() => adjustInfrastructure('roads', 1)}>+</button>
        </div>
      </div>
      
      <div class="infrastructure-item">
        <span class="infrastructure-label">Railroads</span>
        <div class="infrastructure-controls">
          <button class="infra-button" on:click={() => adjustInfrastructure('railroads', -1)}>-</button>
          <span class="infra-count">{infrastructure.railroads}</span>
          <button class="infra-button" on:click={() => adjustInfrastructure('railroads', 1)}>+</button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- History Panel -->
  <div class="stats-panel history-panel">
    <h2 class="panel-title">Action History</h2>
    
    <div class="history-list">
      {#each history as item}
        <div class="history-item">
          <div class="history-action">{item.action}</div>
          <div class="history-effect">{item.effect}</div>
          <div class="history-time">{new Date(item.timestamp).toLocaleTimeString()}</div>
        </div>
      {/each}
    </div>
  </div>
</div>
