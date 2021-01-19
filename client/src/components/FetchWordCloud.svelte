<script lang="ts">
    import ImportanceContext from "./ImportanceContext.svelte";

    export let unit: number;
    export let label: number | string | null = null;
    export let importances: number[];
    export let currIdx: number;
    export let selected: boolean;
    export let width: number | string = "100%";
    export let height: number | string = "100%";
    export let importanceIconWidth = 30; // Px. Ignored if no imporances given. Used for width and height
    export let importanceIconHeight = 40; // Px. Ignored if no imporances given. Used for width and height

    $: filename = `wordclouds/cloud_unit_${unit}.png`;
    $: displayLabel = label == null ? unit : label
</script>

<style lang="postcss">
    .unit-title {
        @apply m-0 p-2 text-2xl font-bold underline;
    }

    .selected {
        text-decoration-color: coral;
        color: coral;
    }
</style>

<div class="relative">
    <div>
        <div class="grid grid-cols-6 gap-0">
            {#if importances}
                <div class="unit-title col-start-1 col-end-6 lg:col-end-5" class:selected>
                    Neuron
                    {displayLabel}
                </div>
                <div class="col-start-6 lg:col-start-5 col-end-7">
                    <div class="">
                        <ImportanceContext
                            {importances}
                            {currIdx}
                            height={importanceIconHeight}
                            width={importanceIconWidth} />
                    </div>
                </div>
            {:else}
                <div
                    class="unit-title col-start-1 col-end-7 text-center"
                    class:selected>
                    Neuron
                    {displayLabel}
                </div>
            {/if}
        </div>
    </div>
    <img
        src={filename}
        alt={`Word Cloud for Neuron ${displayLabel}`}
        {width}
        {height}
        class="overflow-hidden" />
</div>
