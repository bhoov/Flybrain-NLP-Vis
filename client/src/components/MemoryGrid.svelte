<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type * as tp from "../types";
    import * as d3 from "d3"
    const dispatch = createEventDispatcher();

    // I need additional information about kohonen layout and opacity of each cell
    export let cells: tp.MemActivation[];
    export let cellWidth: number = 10;
    export let cellHeight: number = null;
    export let selectedCell: number = null;
    let hoveredCell: number = null;

    if (cellHeight == null) cellHeight = cellWidth;

    $: nCols = Math.floor(Math.sqrt(cells.length));
    $: svgWidth = cellWidth * nCols;
    $: svgHeight = cellHeight * Math.ceil(cells.length / nCols);

    // Why is scale not being detected by d3 types?
    //@ts-ignore
    $: opacityScale = d3.scaleLinear().domain([0, d3.max(cells.map(c => c.activation))]).range([0.1, 1])
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
        {#each cells as cell, i}
            <rect
                transform={`translate(${cellWidth * (cell.head % nCols)}, ${cellHeight * (Math.floor(cell.head / nCols))})`}
                class:hovered={cell.head == hoveredCell}
                class:selected={cell.head == selectedCell}
                width={cellWidth}
                height={cellHeight}
                on:click={() => {
                    if (selectedCell == cell.head) {
                        selectedCell = null;
                    }
                    else {
                        selectedCell = cell.head;
                    }
                    dispatch('cellClick', cell);
                }}
                on:mouseover={() => {
                    hoveredCell = cell.head;
                }}
                on:mouseout={() => {
                    hoveredCell = null;
                }} 
                style={`opacity: ${opacityScale(cell.activation)}`}
                />
        {/each}
    </g>
</svg>
