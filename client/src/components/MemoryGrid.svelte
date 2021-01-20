<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import FetchWordCloud from "./FetchWordCloud.svelte";
    import tippy from "../etc/mytippy";
    import * as d3 from "d3";

    const dispatch = createEventDispatcher();

    // I need additional information about kohonen layout and opacity of each cell
    export let activations: number[];
    export let neuronLabels: number[]; // Use as labels for each neuron. If not provided, name neurons based on index of activations
    export let cellRadius: number = 7;
    export let selectedCell: number;
    export let loading = false;
    export let hoveredCell: number | null = null;
    export let maxOpacity: number = 1;
    export let allowInteraction: boolean = true;


    function tippyProps(unit: number, label: number) {
        const width = 250,
            height = 250;

        const content = `
            <div class="inner-tippy-content" flybrain-unit="${unit}">
                <div class="w-full text-center m-0 p-0 text-2xl font-bold underline">Neuron ${label}</div>
                <img data-src="wordclouds/cloud_unit_${unit}.png" alt="Concepts for neuron ${label}" width="${width}px" height="${height}px"/>
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

    $: nHeads = neuronLabels.length;
    $: nCols = Math.floor(Math.sqrt(nHeads));
    $: svgWidth = cellRadius * 2 * nCols;
    $: svgHeight = cellRadius * 2 * Math.ceil(nHeads / nCols);

    $: opacityScale = d3
        .scaleLinear()
        .domain([0, d3.max(activations)])
        .range([0.1, maxOpacity]);
</script>

<style>
    .primary {
        fill: black;
        stroke-width: 3;
        stroke: white;
    }

    *:focus {
        outline: 0;
    }

    .overlay {
        fill: none;
    }
    .selected {
        stroke: coral;
        stroke-width: 3;
        opacity: 1;
    }

    .hovered {
        stroke: cyan;
        stroke-width: 3;
        opacity: 1;
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
            {#each neuronLabels as neuron, i}
                <!-- Main circle -->
                <circle
                    use:tippy={tippyProps(neuron, i)}
                    class="primary"
                    cx={cellRadius * 2 * (i % nCols) + cellRadius}
                    cy={cellRadius * 2 * Math.floor(i / nCols) + cellRadius}
                    r={cellRadius}
                    on:click={() => (allowInteraction && (selectedCell = neuron))}
                    on:mouseover={() => {
                        hoveredCell = neuron;
                    }}
                    on:mouseout={() => {
                        hoveredCell = null;
                    }}
                    style={`opacity: ${opacityScale(activations[neuron])}`} />

                <!-- Overlay circle -->
                <circle
                    class:hovered={neuron == hoveredCell}
                    class:selected={neuron == selectedCell}
                    class="overlay"
                    cx={cellRadius * 2 * (i % nCols) + cellRadius}
                    cy={cellRadius * 2 * Math.floor(i / nCols) + cellRadius}
                    r={cellRadius}/>
            {/each}
        </g>
    </svg>
</div>
