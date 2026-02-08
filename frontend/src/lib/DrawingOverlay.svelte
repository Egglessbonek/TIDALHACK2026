<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';

  let visible = true;

  onMount(() => {
    // After animation completes, remove the overlay
    setTimeout(() => {
      visible = false;
    }, 2500);
  });
</script>

{#if visible}
  <div 
    class="drawing-overlay"
    out:fade={{ duration: 500 }}
  >
    <svg class="drawing-svg" preserveAspectRatio="none" viewBox="0 0 100 100">
      <defs>
        <mask id="drawing-mask">
          <rect width="100%" height="100%" fill="white" />
          
          <!-- Animated scribble strokes that reveal the content -->
          <g fill="none" stroke="black" stroke-width="8" stroke-linecap="round">
            <!-- Diagonal strokes -->
            <path d="M 0,0 L 20,20" class="stroke stroke-1" />
            <path d="M 20,0 L 40,20" class="stroke stroke-2" />
            <path d="M 40,0 L 60,20" class="stroke stroke-3" />
            <path d="M 60,0 L 80,20" class="stroke stroke-4" />
            <path d="M 80,0 L 100,20" class="stroke stroke-5" />
            
            <path d="M 0,20 L 20,40" class="stroke stroke-6" />
            <path d="M 20,20 L 40,40" class="stroke stroke-7" />
            <path d="M 40,20 L 60,40" class="stroke stroke-8" />
            <path d="M 60,20 L 80,40" class="stroke stroke-9" />
            <path d="M 80,20 L 100,40" class="stroke stroke-10" />
            
            <path d="M 0,40 L 20,60" class="stroke stroke-11" />
            <path d="M 20,40 L 40,60" class="stroke stroke-12" />
            <path d="M 40,40 L 60,60" class="stroke stroke-13" />
            <path d="M 60,40 L 80,60" class="stroke stroke-14" />
            <path d="M 80,40 L 100,60" class="stroke stroke-15" />
            
            <path d="M 0,60 L 20,80" class="stroke stroke-16" />
            <path d="M 20,60 L 40,80" class="stroke stroke-17" />
            <path d="M 40,60 L 60,80" class="stroke stroke-18" />
            <path d="M 60,60 L 80,80" class="stroke stroke-19" />
            <path d="M 80,60 L 100,80" class="stroke stroke-20" />
            
            <path d="M 0,80 L 20,100" class="stroke stroke-21" />
            <path d="M 20,80 L 40,100" class="stroke stroke-22" />
            <path d="M 40,80 L 60,100" class="stroke stroke-23" />
            <path d="M 60,80 L 80,100" class="stroke stroke-24" />
            <path d="M 80,80 L 100,100" class="stroke stroke-25" />
          </g>
          
          <!-- Fill that grows to reveal everything -->
          <rect width="100%" height="100%" fill="black" class="reveal-rect" />
        </mask>
      </defs>
      
      <rect width="100%" height="100%" fill="white" mask="url(#drawing-mask)" />
    </svg>
  </div>
{/if}

<style>
  .drawing-overlay {
    position: fixed;
    inset: 0;
    z-index: 100;
    pointer-events: none;
  }

  .drawing-svg {
    width: 100%;
    height: 100%;
  }

  /* Animate each stroke with staggered timing */
  .stroke {
    stroke-dasharray: 30;
    stroke-dashoffset: 30;
    animation: drawStroke 0.3s ease-out forwards;
  }

  .stroke-1  { animation-delay: 0s; }
  .stroke-2  { animation-delay: 0.05s; }
  .stroke-3  { animation-delay: 0.1s; }
  .stroke-4  { animation-delay: 0.15s; }
  .stroke-5  { animation-delay: 0.2s; }
  .stroke-6  { animation-delay: 0.25s; }
  .stroke-7  { animation-delay: 0.3s; }
  .stroke-8  { animation-delay: 0.35s; }
  .stroke-9  { animation-delay: 0.4s; }
  .stroke-10 { animation-delay: 0.45s; }
  .stroke-11 { animation-delay: 0.5s; }
  .stroke-12 { animation-delay: 0.55s; }
  .stroke-13 { animation-delay: 0.6s; }
  .stroke-14 { animation-delay: 0.65s; }
  .stroke-15 { animation-delay: 0.7s; }
  .stroke-16 { animation-delay: 0.75s; }
  .stroke-17 { animation-delay: 0.8s; }
  .stroke-18 { animation-delay: 0.85s; }
  .stroke-19 { animation-delay: 0.9s; }
  .stroke-20 { animation-delay: 0.95s; }
  .stroke-21 { animation-delay: 1s; }
  .stroke-22 { animation-delay: 1.05s; }
  .stroke-23 { animation-delay: 1.1s; }
  .stroke-24 { animation-delay: 1.15s; }
  .stroke-25 { animation-delay: 1.2s; }

  /* The final reveal fills in the rest */
  .reveal-rect {
    opacity: 0;
    animation: revealFill 0.8s 1.5s ease-out forwards;
  }

  @keyframes drawStroke {
    to {
      stroke-dashoffset: 0;
    }
  }

  @keyframes revealFill {
    to {
      opacity: 1;
    }
  }
</style>
