<script lang="ts">
    import { onMount } from "svelte";
    import ImportanceContext from "./ImportanceContext.svelte";

    export let unit: number;
    export let importances: number[];
    export let currIdx: number;
    export let width = 400;
    export let height = 300;
    export let importanceIconWidth = 30; // Px. Ignored if no imporances given. Used for width and height
    export let importanceIconHeight = 40; // Px. Ignored if no imporances given. Used for width and height
    $: filename = `wordclouds/cloud_unit_${unit}.png`;
</script>

<style lang="postcss">
    .float-icon {
        position: absolute;
        left: 10px;
        top: 10px;
        z-index: 10;
        /* background-color: #5552; */
        border-radius: 4px;
        border: 1px solid rgba(60, 60, 60, 0.3);
        padding: 0px 5px;
        /* margin: 2px;  */
    }
</style>

<div class="relative">
    <img src={filename} alt={`Word Cloud for Unit ${unit}`} {width} {height} />
    {#if importances}
        <div class="float-icon">
            <ImportanceContext
                {importances}
                {currIdx}
                height={importanceIconHeight}
                width={importanceIconWidth} />
        </div>
    {/if}
</div>