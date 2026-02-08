<script>
  import { onMount } from 'svelte';
  import rough from 'roughjs';

  let canvas;
  let isNightMode = false;

  export { isNightMode };

  function drawPaperTexture() {
    if (!canvas) return;
    
    const rc = rough.canvas(canvas);
    const ctx = canvas.getContext('2d');
    
    // Set canvas to full window size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Fill with blue paper color
    const paperColor = isNightMode ? '#4a6b8a' : '#87CEEB';
    ctx.fillStyle = paperColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Graph paper settings
    const gridSize = 20; // Size of each grid square
    const lineColor = isNightMode ? '#3a5a7a' : '#6db8e8';
    const heavyLineColor = isNightMode ? '#2a4a6a' : '#5da8d8';
    
    // Draw vertical lines
    for (let x = 0; x <= canvas.width; x += gridSize) {
      const isHeavyLine = x % (gridSize * 5) === 0;
      rc.line(x, 0, x, canvas.height, {
        stroke: isHeavyLine ? heavyLineColor : lineColor,
        strokeWidth: isHeavyLine ? 1.5 : 0.8,
        roughness: 0.5,
        bowing: 0.3
      });
    }
    
    // Draw horizontal lines
    for (let y = 0; y <= canvas.height; y += gridSize) {
      const isHeavyLine = y % (gridSize * 5) === 0;
      rc.line(0, y, canvas.width, y, {
        stroke: isHeavyLine ? heavyLineColor : lineColor,
        strokeWidth: isHeavyLine ? 1.5 : 0.8,
        roughness: 0.5,
        bowing: 0.3
      });
    }
  }

  onMount(() => {
    drawPaperTexture();
    
    const handleResize = () => {
      drawPaperTexture();
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });

  // Redraw when night mode changes
  $: if (canvas) {
    drawPaperTexture();
  }
</script>

<canvas bind:this={canvas} class="paper-canvas"></canvas>

<style>
  .paper-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    pointer-events: none;
  }
</style>
