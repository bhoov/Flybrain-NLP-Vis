<script lang="ts">
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher()

    // I need additional information about kohonen layout and opacity of each cell
    export let cells: number[][];
    export let cellWidth: number = 10;
    export let cellHeight: number = null;
    export let selectedCell: number = null

    if (cellHeight == null) cellHeight = cellWidth;

    let hoveredCell: number = null

    $: svgHeight = cellHeight * cells.length;
    $: svgWidth = cellWidth * cells[0].length;
</script>

<style>
    rect {
        fill: black;
        opacity: 1;
        stroke-width: 2;
        stroke: white;
    }

    .hovered {
        fill: cyan;
    }

    .selected {
        fill: coral;
    }
</style>

<svg width={svgWidth} height={svgHeight}>
    <g>
        {#each cells as row, i}
            {#each row as cell, j}
                <rect
                    transform={`translate(${cellWidth * i}, ${cellHeight * j})`}
                    class:hovered={cell == hoveredCell}
                    class:selected={cell == selectedCell}
                    width={cellWidth}
                    height={cellHeight} 
                    on:click={() => {
                        selectedCell = cell;
                        dispatch("cellClick", {i, j, cell})
                    }}
                    on:mouseover={() => {
                        hoveredCell = cell
                    }}
                    on:mouseout={() => {
                        hoveredCell = null
                    }}
                    />
            {/each}
        {/each}
    </g>
</svg>
