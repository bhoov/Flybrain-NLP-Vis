<script lang="ts">
    import ImportanceContext from "./ImportanceContext.svelte";

    export let unit: number;
    export let importances: number[];
    export let currIdx: number;
    export let selected: boolean;
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

    .unit-title {
        @apply w-full text-center m-0 p-0 text-2xl font-bold underline;
    }

    .selected {
        text-decoration-color: coral;
    }
</style>

<div class="relative">
    <div>
        <div class="unit-title" class:selected={selected}>Neuron {unit}</div>
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
    <img src={filename} alt={`Word Cloud for Unit ${unit}`} {width} {height} class="overflow-hidden"/>
</div>
