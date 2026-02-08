<script>
  import { onMount } from 'svelte';
  import Dashboard from '$lib/Dashboard.svelte';
  import crayonSky from '$lib/assets/images/crayon-sky.png';
  import crayonSky2 from '$lib/assets/images/sky-texture-2.png';
  import crayonGrass from '$lib/assets/images/crayon-grass.png';
  import crayonGrass2 from '$lib/assets/images/crayon-grass-2.png';

  let currentPage = 0; // 0 = left, 1 = center, 2 = right, 3 = dashboard
  const totalPages = 4;

  function handleKeydown(event) {
    if (event.key === 'ArrowLeft') {
      currentPage = Math.max(0, currentPage - 1);
    } else if (event.key === 'ArrowRight') {
      currentPage = Math.min(totalPages - 1, currentPage + 1);
    }
  }

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => {
      window.removeEventListener('keydown', handleKeydown);
    };
  });
</script>

<style>
  .background-container {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: 0;
  }

  .pages-container {
    position: absolute;
    inset: 0;
    width: 400%;
    height: 100%;
    display: flex;
    transition: transform 0.5s ease-in-out;
  }

  .page {
    position: relative;
    width: 25%;
    height: 100%;
    flex-shrink: 0;
  }

  .background-layer {
    position: absolute;
    inset: 0;
  }

  :global(.scroll-track) {
    position: absolute;
    inset: 0;
    display: flex;
    width: calc(var(--segment-width) * 2);
    height: 100%;
    will-change: transform;
    transform: translate3d(0, 0, 0);
  }

  :global(.scroll-segment) {
    flex: 0 0 var(--segment-width);
    height: 100%;
    background-repeat: repeat-x;
    background-position: 0 0;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
  }

  .sky {
    height: 110%;
    width: 110%;
    top: -5%;
    left: -5%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }

  .sky-frame-1 {
    opacity: 1;
    animation: grassSwapOff 4s steps(1, end) infinite;
  }

  .sky-frame-2 {
    opacity: 0;
    animation: grassSwapOn 4s steps(1, end) infinite;
  }

  .static-grass {
    height: 50%;
    bottom: 0;
    width: 120%;
    left: -10%;
    top: auto;
    background-size: cover;
    background-position: center top;
    background-repeat: no-repeat;
  }

  .grass-frame-1 {
    opacity: 1;
    animation: grassSwapOff 2s steps(1, end) infinite;
  }

  .grass-frame-2 {
    opacity: 0;
    animation: grassSwapOn 2s steps(1, end) infinite;
  }

  @keyframes grassSwapOff {
    0%, 49.999% { opacity: 1; }
    50%, 100%   { opacity: 0; }
  }

  @keyframes grassSwapOn {
    0%, 49.999% { opacity: 0; }
    50%, 100%   { opacity: 1; }
  }

  :global(.scroll-sky-track) {
    animation: scrollTrackRight calc((var(--segment-width) / var(--sky-scroll-speed)) * 1s) linear infinite;
  }

  .scroll-sky {
    background-size: auto 80%;
  }

  /* Two identical segments; move exactly 100vw for a seamless loop. */
  @keyframes scrollTrackRight {
    from { transform: translate3d(calc(-1 * var(--segment-width)), 0, 0); }
    to   { transform: translate3d(0, 0, 0); }
  }

  @media (hover: none) and (pointer: coarse) {
    :global(.scroll-track) {
      animation: none;
      transform: none;
      width: 100%;
    }

    :global(.scroll-segment) {
      flex: 1 1 auto;
      width: 100%;
    }

    :global(.scroll-track) .scroll-segment + .scroll-segment {
      display: none;
    }

    :global(.scroll-sky) {
      animation: fallbackSky calc((var(--segment-width) / var(--sky-scroll-speed)) * 1s) linear infinite;
    }
  }

  @supports (-moz-appearance: none) {
    :global(.scroll-track) {
      animation: none;
      transform: none;
      width: 100%;
    }

    :global(.scroll-segment) {
      flex: 1 1 auto;
      width: 100%;
    }

    :global(.scroll-track) .scroll-segment + .scroll-segment {
      display: none;
    }

    :global(.scroll-sky) {
      animation: fallbackSky calc((var(--segment-width) / var(--sky-scroll-speed)) * 1s) linear infinite;
    }
  }

  @keyframes fallbackSky {
    from { background-position: calc(-1 * var(--segment-width)) 0; }
    to   { background-position: 0 0; }
  }
</style>


<div class="background-container">
  <div class="pages-container" style="transform: translateX(-{currentPage * 25}%);">
    <!-- Page 1 (Left) -->
    <div class="page">
      <div class="background-layer sky sky-frame-1" style="background-image: url('{crayonSky}');"></div>
      <div class="background-layer sky sky-frame-2" style="background-image: url('{crayonSky2}');"></div>
      <div class="background-layer static-grass grass-frame-1" style="background-image: url('{crayonGrass}');"></div>
      <div class="background-layer static-grass grass-frame-2" style="background-image: url('{crayonGrass2}');"></div>
    </div>
    
    <!-- Page 2 (Center) -->
    <div class="page">
      <div class="background-layer sky sky-frame-1" style="background-image: url('{crayonSky}');"></div>
      <div class="background-layer sky sky-frame-2" style="background-image: url('{crayonSky2}');"></div>
      <div class="background-layer static-grass grass-frame-1" style="background-image: url('{crayonGrass}');"></div>
      <div class="background-layer static-grass grass-frame-2" style="background-image: url('{crayonGrass2}');"></div>
    </div>
    
    <!-- Page 3 (Right) -->
    <div class="page">
      <div class="background-layer sky sky-frame-1" style="background-image: url('{crayonSky}');"></div>
      <div class="background-layer sky sky-frame-2" style="background-image: url('{crayonSky2}');"></div>
      <div class="background-layer static-grass grass-frame-1" style="background-image: url('{crayonGrass}');"></div>
      <div class="background-layer static-grass grass-frame-2" style="background-image: url('{crayonGrass2}');"></div>
    </div>
    
    <!-- Page 4 (Dashboard) -->
    <div class="page">
      <div class="background-layer sky sky-frame-1" style="background-image: url('{crayonSky}');"></div>
      <div class="background-layer sky sky-frame-2" style="background-image: url('{crayonSky2}');"></div>
      <div class="background-layer static-grass grass-frame-1" style="background-image: url('{crayonGrass}');"></div>
      <div class="background-layer static-grass grass-frame-2" style="background-image: url('{crayonGrass2}');"></div>
      <Dashboard />
    </div>
  </div>
</div>

