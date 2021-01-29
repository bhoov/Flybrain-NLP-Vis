<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    export let maxWidth: number = 350;
    export let maxHeight: number = 350;
    export let margin = {
        top: 15,
        right: 50,
        bottom: 15,
        left: 150,
    };

    interface Data {
        name: string
        value: number
    }
    export let data: Data[] = [];

    $: width = maxWidth - margin.left - margin.right;
    $: height = maxHeight - margin.top - margin.bottom;

    $: xScale = d3
        .scaleLinear()
        .range([0, width])
        .domain([
            0,
            d3.max(data, function (d) {
                return d.value;
            }),
        ]);

    $: yScale = d3
        .scaleBand()
        .range([0, height])
        .padding(0.1)
        .domain(data.map((d) => d.name));

    //make y axis to show bar names
    let leftAxis;
    $: yAxis = d3.axisLeft(yScale);
    $: leftAxis != undefined && yAxis(d3.select(leftAxis));

    onMount(() => {
        yAxis(d3.select(leftAxis));
    });
</script>

<style lang="postcss">
    .bar {
        fill: #5f89ad;
    }

    .axis {
        font-size: 16px;
    }

    .axis path,
    .axis line {
        fill: none;
        display: none;
    }
</style>

<svg width="100%" height="100%" viewBox={`0 0 ${maxWidth} ${maxHeight}`}>
    <g transform={`translate(${margin.left}, ${margin.top})`}>
        <g bind:this={leftAxis} class="axis"/>
        {#each data as d,i}
            <rect
                class="bar"
                y={yScale(d.name)}
                height={yScale.bandwidth()}
                x={0}
                width={xScale(d.value)} 
                />
        {/each}
    </g>
</svg>
