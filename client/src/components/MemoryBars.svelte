<script lang="ts">
    import * as d3 from "d3"
    import * as tp from "../types"

    export let barInfo: tp.MemActivation[] = []
    export let width = 250;
    export let height = 150;
    export let padding = 10
    export let hoveredHead: number

    $: xScale = d3.scaleBand().domain(barInfo.map((d, i) => `${i}`)).range([padding, width - padding]).paddingInner(0.2).paddingOuter(0.3)
    $: yScale = d3.scaleLinear().domain([0, d3.max(barInfo.map(b => b.activation))]).range([height - padding, padding])
</script>

<style lang="postcss">
    .hovered {
        fill: cyan !important;
    }
</style>

<svg>
    <g>
        {#each barInfo as bar, i}
            <rect 
                class:hovered={hoveredHead == bar.head}
                x={xScale(`${i}`)}
                y={yScale(bar.activation)}
                rx=5
                width={xScale.bandwidth()}
                height={height - yScale(bar.activation)}
                fill="steelblue"
                opacity=1
                on:mouseover={() => hoveredHead = bar.head}
                on:mouseout={() => hoveredHead = null}
            />
        {/each}
    </g>
</svg>
