<script lang="ts">
    import FetchWordCloud from "./FetchWordCloud.svelte";
    import { toggle } from "../etc/Util";

    export let heads: number[] = [];
    export let labels: number[] | string[] | null = null;
    export let importances: number[] = [];
    export let offensiveNeurons: Set<number>
    export let hoveredHead: number | null = null;
    export let selectedHead: number = null;
    export let mouseable: boolean = true
    export let smallTitle: boolean = false // If true, display wordclouds with small titles

    $: displayLabels = labels == null ? heads : labels
</script>

<style lang="postcss">
    .status {
        margin: auto;
        color: red;
        vertical-align: middle;
    }

    .cloud {
        border: 4px solid #3c3c3c3c;
        border-radius: 1rem;
        margin: 0.4rem 0.25rem;
        max-height: 300px;
        max-width: 250px;
    }

    .hovered {
        transition: font-size 0.1s;
        border-color: var(--hovered);
    }

    .selected {
        box-shadow: 0px 0px 1rem 5px var(--selected);
    }
</style>

{#each heads as head, i}
        <div
            class:hovered={head == hoveredHead}
            class:selected={head == selectedHead}
            class="cloud border-2 border-gray-800 place-self-center w-full"
            on:mouseover={() => (mouseable && (hoveredHead = head))}
            on:mouseout={() => (mouseable && (hoveredHead = undefined))}
            on:click={() => (mouseable && (selectedHead = head))}
            >
            <FetchWordCloud
                unit={head}
                label={displayLabels[i]}
                hideContent={offensiveNeurons ? offensiveNeurons.has(displayLabels[i]) : false}
                {importances}
                currIdx={i}
                {smallTitle}
                selected={head == selectedHead} />
        </div>
{/each}
