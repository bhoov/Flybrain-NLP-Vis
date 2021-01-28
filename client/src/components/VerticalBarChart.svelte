<script lang="ts">
    import {onMount} from "svelte"
    import * as d3 from "d3";
    import * as tp from "../types";

    export let data: tp.MemActivation[] = [];
    export let maxWidth = 350;
    export let maxHeight = 150;
    export let padding = 0.2;
    export let hoveredHead: number;
    export let margin = {
        top: 15,
        right: 50,
        bottom: 50,
        left: 10,
    };
    export let showTickLabels = false;

    $: width = maxWidth - margin.left - margin.right;
    $: height = maxHeight - margin.top - margin.bottom;

    $: xScale = d3
        .scaleBand()
        .domain(data.map((d, i) => `${d.head + 1}`))
        .range([0, width])
        .padding(padding);

    $: yScale = d3
        .scaleLinear()
        .domain([0, d3.max(data, (b) => b.activation)])
        .range([height, 0]);

    //make y axis to show bar names
    let bottomAxis;
    $: xAxis = d3.axisBottom(xScale);
    $: bottomAxis != undefined && xAxis(d3.select(bottomAxis));

    onMount(() => {
        //@ts-ignore
        const myAxis = d3.select(bottomAxis)
        if (showTickLabels) {
            //@ts-ignore
            myAxis.tickFormat('')
        }
        xAxis(myAxis);
    });
</script>

<style lang="postcss">
    .hovered {
        fill: var(--hovered) !important;
    }
</style>

<svg width={maxWidth} height={maxHeight}>
    <g transform={`translate(${margin.left}, ${margin.top})`}>
        <g bind:this={bottomAxis} class="axis" transform={`translate(0, ${height})`}/>
        {#each data as bar, i}
            <rect
                class:hovered={hoveredHead == bar.head}
                x={xScale(`${bar.head + 1}`)}
                y={yScale(bar.activation)}
                rx="5"
                width={xScale.bandwidth()}
                height={height - yScale(bar.activation)}
                fill="steelblue"
                opacity="1"
                on:mouseover={() => (hoveredHead = bar.head)}
                on:mouseout={() => (hoveredHead = null)} />
        {/each}
    </g>
</svg>
