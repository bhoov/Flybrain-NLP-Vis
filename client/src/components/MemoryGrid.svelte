<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type * as tp from "../types";
    import * as d3 from "d3"
    import { toggle } from "../etc/Util";

    const dispatch = createEventDispatcher();

    // I need additional information about kohonen layout and opacity of each cell
    export let activations: number[];
    export let headOrdering: number[];
    export let cellRadius: number = 7;
    export let selectedCell: number;
    export let hoveredCell: number;

    $: nHeads = headOrdering.length
    $: nCols = Math.floor(Math.sqrt(nHeads));
    $: svgWidth = cellRadius * 2 * nCols;
    $: svgHeight = cellRadius * 2 * Math.ceil(nHeads / nCols);

    $: opacityScale = d3.scaleLinear().domain([0, d3.max(activations)]).range([0.1, 1])
</script>

<style>
    circle {
        fill: black;
        stroke-width: 2;
        stroke: white;
    }

    .selected {
        fill: coral !important;
        opacity: 1 !important;
    }

    .hovered {
        fill: cyan;
        opacity: 1;
    }

</style>

<svg width={svgWidth} height={svgHeight}>
    <g>
        {#each headOrdering as head, i}
            <circle
                class:hovered={head == hoveredCell}
                class:selected={head == selectedCell}
                cx={cellRadius * 2 * (i % nCols) + cellRadius}
                cy={cellRadius * 2 * (Math.floor(i / nCols)) + cellRadius}
                r={cellRadius}
                on:click={() => {
                    let deselect = false
                    if (selectedCell == head) {
                        selectedCell = null; 
                        deselect = true
                    }
                    else {
                        selectedCell = head;
                        deselect = false
                    }
                    dispatch('cellClick', {head, activation: activations[i], deselect});
                }}
                on:mouseover={() => {
                    hoveredCell = head;
                }}
                on:mouseout={() => {
                    hoveredCell = null;
                }} 
                style={`opacity: ${opacityScale(activations[head])}`}
                />
        {/each}
    </g>
</svg>
