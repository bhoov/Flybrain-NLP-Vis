<script lang="ts">
    import * as d3 from "d3";
    import cloud from "d3-cloud";
    import type { Word } from "d3-cloud";
    import type * as tp from "../types";

    export let concepts: tp.Concept[] = [];
    let isMounted: boolean = false;
    $: contributions = concepts.map((d) => d.contribution);

    $: sizeScale = d3
        //@ts-ignore
        .scaleLinear()
        .domain([0, d3.max(contributions)])
        .range([10, 100]);

    $: words = concepts.map((c) => {
        return {
            text: c.token,
            size: sizeScale(c.contribution),
        } as Word;
    });

    let displayWords: Word[] | null = null;

    function redefineWords(newWords: Word[]) {
        displayWords = newWords;
    }

    $: layout = cloud()
        .size([500, 500])
        .words(words)
        .padding(5)
        .rotate(function () {
            return ~~(Math.random() * 2) * 90;
        })
        .font("Impact")
        .fontSize(function (d) {
            return d.size;
        })
        .on("end", redefineWords)
        .start();
</script>

<div class="cloud">
    {#if displayWords != null}
        <svg width={layout.size()[0]} height={layout.size()[1]}>
            <g
                transform={`translate(${layout.size()[0] / 2},${layout.size()[1] / 2})`}>
                {#each displayWords as word (word.text)}
                    <text
                        font-size={word.size + 'px'}
                        font-family={word.font}
                        text-anchor="middle"
                        transform={`translate(${word.x}, ${word.y})rotate(${word.rotate})`}>
                        {word.text}
                    </text>
                {/each}
            </g>
        </svg>
    {/if}
</div>
