<script lang="ts">
    import ImportanceContext from "./ImportanceContext.svelte";

    export let unit: number;
    export let label: number | string | null = null;
    export let importances: number[] = null;
    export let currIdx: number = null;
    export let selected: boolean = false;
    export let width: number | string | null = "100%";
    export let hideContent: boolean = false; // Some neurons learn offensive concepts. Mask these wordclouds
    export let importanceIconWidth = 30; // Px. Ignored if no imporances given. Used for width and height
    export let importanceIconHeight = 40; // Px. Ignored if no imporances given. Used for width and height
    export let smallTitle = false // If true, don't format title as large text
    let showClean = false;

    $: displayName = showClean ? "#" : "Neuron "
    $: titleClass = `unit-title ${smallTitle ? "text-xs" : "text-lg"}`

    $: filename = `wordclouds/cloud_unit_${unit}.png`;
    $: displayLabel = label == null ? unit : label
</script>

<style lang="postcss">
    .unit-title {
        @apply m-0 font-bold underline;
    }

    .selected {
        text-decoration-color: var(--selected);
        color: var(--selected);
    }
</style>

<div class="relative">
    <div>
            {#if importances}
            <div class="flex justify-between items-center h-8">
                <div class={titleClass} class:selected>
                    {displayName}{displayLabel}
                </div>
                <div class="mr-3">
                        <ImportanceContext
                            {importances}
                            {currIdx}
                            height={importanceIconHeight}
                            width={importanceIconWidth} />
                </div>
            </div>
            {:else}
                <div
                    class={titleClass}
                    class:selected>
                    {displayName}{displayLabel}
                </div>
            {/if}
    </div>

    {#if hideContent}
    <div class="text-center text-xl muted font-bold m-auto">The concepts learned by this neuron are offensive and were manually masked</div>
    {:else}
    <img
        src={filename}
        alt={`Word Cloud for Neuron ${displayLabel}`}
        width={width || ""}
        class="overflow-hidden" />
    {/if}
</div>
