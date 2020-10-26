<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type * as tp from "../types";
    import * as d3 from "d3"
    const dispatch = createEventDispatcher();

    // I need additional information about kohonen layout and opacity of each cell
    export let activations: number[];
    export let headOrdering: number[];
    export let cellWidth: number = 10;
    export let cellHeight: number = null;
    export let selectedCell: number = null;
    let hoveredCell: number = null;

    if (cellHeight == null) cellHeight = cellWidth;

    $: nHeads = headOrdering.length
    $: nCols = Math.floor(Math.sqrt(nHeads));
    $: svgWidth = cellWidth * nCols;
    $: svgHeight = cellHeight * Math.ceil(nHeads / nCols);

    $: opacityScale = d3.scaleLinear().domain([0, d3.max(activations)]).range([0.1, 1])
</script>

<style>
    rect {
        fill: black;
        stroke-width: 2;
        stroke: white;
    }

    .hovered {
        fill: cyan;
        opacity: 1 !important;
    }

    .selected {
        fill: coral;
        opacity: 1 !important;
    }
</style>

<svg width={svgWidth} height={svgHeight}>
    <g>
        {#each headOrdering as head, i}
            <rect
                transform={`translate(${cellWidth * (i % nCols)}, ${cellHeight * (Math.floor(i / nCols))})`}
                class:hovered={head == hoveredCell}
                class:selected={head == selectedCell}
                width={cellWidth}
                height={cellHeight}
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
