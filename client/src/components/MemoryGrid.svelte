<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import FetchWordCloud from "./FetchWordCloud.svelte";
    import FloatWindow from "./FloatWindow.svelte"
    import tippy from "../etc/mytippy";
    import 'tippy.js/themes/light.css';
    import 'tippy.js/themes/translucent.css';

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
    export let strokeWidth = 3;
    export let offensiveNeurons: Set<number>


    function tippyProps(unit: number, label: number) {
        const width = 250,
            height = 250;

        const imgContent = `<img data-src="wordclouds/cloud_unit_${unit}.png" alt="Concepts for neuron ${label}" width="${width}px" height="${height}px"/>`
        const hiddenContent = `<div class="text-center text-l font-bold text-white m-auto">The concepts learned by this neuron are offensive and were manually masked</div>`
        const isOffensiveNeuron = offensiveNeurons && offensiveNeurons.has(label)
        const content = `
            <div class="inner-tippy-content" flybrain-unit="${unit}">
                <div class="w-full text-center m-0 p-0 text-2xl font-bold underline">Neuron ${label}</div>
                ${isOffensiveNeuron ? hiddenContent : imgContent}
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
            theme: "light",
            distance: 1,
            onShow: function (instance) {
                if (!isOffensiveNeuron) {
                    var img = instance.popper.querySelector("img");
                    img.setAttribute("src", img.getAttribute("data-src"));
                }
            },
        };
    }

    $: nHeads = neuronLabels.length;
    $: nCols = Math.floor(Math.sqrt(nHeads));
    // $: svgWidth = (cellRadius + strokeWidth / 2) * 2 * nCols + (2 * strokeWidth);
    // $: svgHeight = (cellRadius + strokeWidth / 2) * 2 * Math.ceil(nHeads / nCols) + (2 * strokeWidth);
    $: svgWidth = (cellRadius) * 2 * nCols + (2 * strokeWidth);
    $: svgHeight = (cellRadius) * 2 * Math.ceil(nHeads / nCols) + (2 * strokeWidth);

    $: opacityScale = d3
        .scaleLinear()
        .domain([0, d3.max(activations)])
        .range([0.1, maxOpacity]);

    // Place the i'th circle in the correct row on the grid
    // $: placeX = (i: number) => strokeWidth + 2 * (cellRadius + strokeWidth / 2) * (i % nCols) + cellRadius 
    $: placeX = (i: number) => strokeWidth + 2 * (cellRadius) * (i % nCols) + cellRadius 

    // Place the i'th circle in the correct row on the grid
    $: placeY = (i: number) => strokeWidth + 2 * (cellRadius) * Math.floor(i / nCols) + cellRadius
</script>

<style lang="postcss">
    .primary {
        fill: black;
        z-index: 1;
        stroke: white;
    }

    *:focus {
        outline: 0;
    }

    .overlay {
        fill: none;
        stroke: none;
    }

    .selected {
        stroke: var(--selected);
        z-index: 2;
        opacity: 1;
    }

    .hovered {
        stroke: var(--hovered);
        opacity: 1;
        z-index: 10;
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

<div class:loading class="h-full">
    <svg width="100%" height="100%" viewBox={`0 0 ${svgWidth} ${svgHeight}`}>
        <g>
            {#each neuronLabels as neuron, i}
                <!-- Main circle -->
                <circle
                    use:tippy={tippyProps(neuron, i)}
                    class="primary"
                    cx={placeX(i)}
                    cy={placeY(i)}
                    r={cellRadius}
                    on:click={() => (allowInteraction && (selectedCell = neuron))}
                    on:mouseover={() => {
                        hoveredCell = neuron;
                    }}
                    on:mouseout={() => {
                        hoveredCell = null;
                    }}
                    style={`opacity: ${opacityScale(activations[neuron])}; stroke-width: 2`} />

                <!-- Overlay circle -->
                <circle
                    class:hovered={neuron == hoveredCell}
                    class:selected={neuron == selectedCell}
                    class="overlay"
                    style={`opacity: ${1}; stroke-width: ${strokeWidth}px`}
                    cx={placeX(i)}
                    cy={placeY(i)}
                    r={cellRadius}/>
            {/each}
        </g>
    </svg>
    <!-- <FloatWindow/> -->
</div>
