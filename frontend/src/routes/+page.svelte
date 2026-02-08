<script lang="ts">
  import BackgroundScroller from '$lib/BackgroundScroller.svelte';
  import DrawingOverlay from '$lib/DrawingOverlay.svelte';
  import paperTexture from '$lib/assets/images/paper-texture.png';
  
  // Night Mode State
  let isNightMode = false;

  function toggleNightMode() {
    isNightMode = !isNightMode;
  }
</script>

<DrawingOverlay />

<div class="page-container" class:night-mode={isNightMode}>
  <!-- Render our animated background component -->
  <BackgroundScroller />
  
  {#if isNightMode}
    <div class="night-tint"></div>
  {/if}

  <button class="mode-toggle" on:click={toggleNightMode} aria-label="Toggle Night Mode">
    {isNightMode ? '☀️ Day' : '🌙 Night'}
  </button>
</div>

<style>
  .page-container {
    width: 100vw;
    height: 100vh;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    user-select: none;
    background-image: url('{paperTexture}');
    background-size: cover;
    background-position: center;
    transition: background-color 0.3s;
  }

  .page-container.night-mode {
    /* Night background color */
    background: transparent;
  }

  .night-tint {
    position: absolute;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.3); /* 40% darker tint */
    z-index: 1; /* Above background (0), below overlay (5) */
    pointer-events: none;
  }

  .mode-toggle {
    position: absolute;
    top: 1rem;  
    right: 1rem;
    z-index: 20;
    padding: 15px;
    font-family: 'Press Start 2P', cursive, sans-serif;
    font-size: 0.8rem;
    cursor: pointer;
    
    color: white;
    text-shadow: 2px 2px 0 rgba(0,0,0,0.7);
    background-color: rgba(0, 0, 0, 0.3);
    border: none;
    border-radius: 4px;
    user-select: text;
    
    transition: background-color 0.2s, transform 0.1s;
  }

  .mode-toggle:hover {
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .mode-toggle:active {
    transform: scale(0.95);
  }
</style>
