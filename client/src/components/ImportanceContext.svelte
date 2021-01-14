<script lang="ts">
    import * as d3 from "d3";

    /**
     * Create a small icon barchart showing how important the concept is to a collection of words
     */
    export let importances: number[]; // Main prop showing height of bars
    export let currIdx: number | null = null; // Which bar to highlight
    export let width: number = 100; // width of SVG
    export let height: number = 100; // height of SVG
    export let barGap = 2; // Gap between bars
    export let barWidth = 10; // Width of each bar
    export let domain: [number, number] | null = null // What should be min/max. If not specified, default to extent of data
    export let minBarHeight = 5; // Minimum height of the bar
    export let maxBarHeight = null; // default to height
    export let rx = 5; // Rounded edges of bars

    if (maxBarHeight == null) {
        maxBarHeight = height;
    }

    $: displayWidth = importances.length * (barWidth + barGap); // For adjusting SVG dynamically
    $: yScale = d3
        .scaleLinear()
        .domain(domain || d3.extent(importances))
        .range([minBarHeight, maxBarHeight]);

</script>

<style>
    rect {
        fill: lightgray;
        stroke: none;
    }

    .me {
        fill: red;
    }
</style>

<svg {width} {height} viewBox={`0 0 ${displayWidth} ${height}`}>
    {#each importances as imp, i}
        <rect
            class:me={i == currIdx}
            x={i * (barWidth + barGap)}
            y={height - yScale(imp)}
            width={barWidth}
            height={yScale(imp)}
            {rx} />
    {/each}
</svg>
