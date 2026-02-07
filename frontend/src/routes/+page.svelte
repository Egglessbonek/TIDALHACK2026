<script lang="ts">
  import { onMount } from 'svelte';
  
  let mounted = false;
  
  onMount(() => {
    mounted = true;
  });
</script>

<main class="min-h-screen p-8 bg-graph-paper">
  <div class="paper-border bg-white p-6 max-w-md mx-auto animate-wobble">
    <h1 class="text-3xl font-bold text-blue-800 mb-4 font-sketch">
      🏗️ Causal Canvas
    </h1>
    
    <div class="space-y-2">
      <p class="text-lg text-gray-700 font-sketch">
        ✅ Tailwind v4 is {mounted ? 'working' : 'loading'}!
      </p>
      <p class="text-sm text-gray-500">
        You should see:
      </p>
      <ul class="text-xs list-disc list-inside text-gray-600">
        <li>Graph paper background</li>
        <li>Wobbling animation</li>
        <li>Hand-drawn border</li>
        <li>Custom sketch fonts</li>
      </ul>
    </div>
    
    <!-- Test Tailwind utility classes -->
    <div class="mt-4 flex gap-2">
      <div class="size-10 bg-red-500 rounded-lg"></div>
      <div class="size-10 bg-green-500 rounded-lg"></div>
      <div class="size-10 bg-blue-500 rounded-lg"></div>
    </div>
    
    <!-- Test button -->
    <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-sketch">
      Start Building!
    </button>
  </div>
</main>
