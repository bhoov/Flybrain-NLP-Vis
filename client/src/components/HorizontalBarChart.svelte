<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    export let maxWidth: number = 400;
    export let maxHeight: number = 300;
    export let margin = {
        top: 15,
        right: 50,
        bottom: 15,
        left: 100,
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
        font-size: 13px;
    }

    .axis path,
    .axis line {
        fill: none;
        display: none;
    }

</style>

<svg width={maxWidth} height={maxHeight}>
    <g transform={`translate(${margin.left}, ${margin.top})`}>
        <g bind:this={leftAxis} class="axis"/>
        {#each data as d, i (d.name)}
            <rect
                class="bar"
                y={yScale(d.name)}
                height={yScale.bandwidth()}
                x={0}
                width={xScale(d.value)} 
                on:mouseover={() => {
                    console.log("My value: ", d.value)
                }}
                />
        {/each}
    </g>
</svg>
