<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import FetchWordCloud from "./FetchWordCloud.svelte";
    import tippy from "../etc/mytippy";
    import * as d3 from "d3";

    const dispatch = createEventDispatcher();

    // I need additional information about kohonen layout and opacity of each cell
    export let activations: number[];
    export let headOrdering: number[];
    export let cellRadius: number = 7;
    export let selectedCell: number;
    export let loading = false;
    export let hoveredCell: number;

    function tippyProps(unit: number) {
        const width = 250,
            height = 250;

        const content = `
            <div class="inner-tippy-content" flybrain-unit="${unit}">
                <div class="w-full text-center m-0 p-0 text-2xl font-bold underline">Neuron ${unit}</div>
                <img data-src="wordclouds/cloud_unit_${unit}.png" alt="Concepts for unit ${unit}" width="${width}px" height="${height}px"/>
            </div>
        `;
        return {
            content,
            placement: "top",
            delay: [20, 20], // show, hide in ms
            // delay: [0, 0], // show, hide in ms
            duration: [100, 0], // show, hide in ms
            // duration: [0, 0], // show, hide in ms
            allowHTML: true,
            hideOnClick: false,
            arrow: true,
            theme: "translucent",
            distance: 1,
            onShow: function (instance) {
                var img = instance.popper.querySelector("img");
                img.setAttribute("src", img.getAttribute("data-src"));
            },
        };
    }

    $: nHeads = headOrdering.length;
    $: nCols = Math.floor(Math.sqrt(nHeads));
    $: svgWidth = cellRadius * 2 * nCols;
    $: svgHeight = cellRadius * 2 * Math.ceil(nHeads / nCols);

    $: opacityScale = d3
        .scaleLinear()
        .domain([0, d3.max(activations)])
        .range([0.1, 1]);
</script>

<style>
    circle {
        fill: black;
        stroke-width: 2;
        stroke: white;
    }

    .hovered {
        stroke: rgba(0, 255, 255);
        stroke-opacity: 1 !important;
        stroke-width: 2;
        /* opacity: 1 !important; */
    }
    .selected {
        fill: coral !important;
        opacity: 1 !important;
    }

    .loading {
        transform: scale(1);
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.7);
        }

        70% {
            transform: scale(1);
            box-shadow: 0 0 0 10px rgba(0, 0, 0, 0);
        }

        100% {
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
        }
    }
</style>

<div class:loading>
    <svg width={svgWidth} height={svgHeight}>
        <g>
            {#each headOrdering as head, i}
                <circle
                    class:hovered={head == hoveredCell}
                    class:selected={head == selectedCell}
                    use:tippy={tippyProps(head)}
                    cx={cellRadius * 2 * (i % nCols) + cellRadius}
                    cy={cellRadius * 2 * Math.floor(i / nCols) + cellRadius}
                    r={cellRadius}
                    on:click={() => {
                        let deselect = false;
                        if (selectedCell == head) {
                            selectedCell = null;
                            deselect = true;
                        } else {
                            selectedCell = head;
                            deselect = false;
                        }
                        dispatch('cellClick', {
                            head,
                            activation: activations[i],
                            deselect,
                        });
                    }}
                    on:mouseover={() => {
                        hoveredCell = head;
                    }}
                    on:mouseout={() => {
                        hoveredCell = null;
                    }}
                    style={`opacity: ${opacityScale(activations[head])}`} />
            {/each}
        </g>
    </svg>
</div>
