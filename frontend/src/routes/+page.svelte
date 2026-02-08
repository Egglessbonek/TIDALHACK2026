<script lang="ts">
  import BackgroundScroller from '$lib/BackgroundScroller.svelte';
  import DrawingOverlay from '$lib/DrawingOverlay.svelte';
  import paperTexture from '$lib/assets/images/paper-texture.png';
</script>

<DrawingOverlay />

<div class="page-container">
  <!-- Render our animated background component -->
  <BackgroundScroller />
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
</style>
