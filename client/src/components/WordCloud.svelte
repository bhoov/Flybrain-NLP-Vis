<script lang="ts">
    import * as d3 from "d3";
    import cloud from "d3-cloud";
    import type { Word } from "d3-cloud";
    import type * as tp from "../types";

    export let concepts: tp.Concept[] = [];
    export let width: number = 500;
    export let height: number = 500;
    export let minFontSize = 20; // Let font get no smaller than this
    export let maxFontSize = null; // Maximum size of font. If not provided, default to 1/5 of min(width, height)

    // Sometimes not all words display. Iteratively shrink size difference until all words fit
    $: contributions = concepts.map((d) => d.contribution);

    $: maxPxSize = maxFontSize == null ? d3.min([width, height]) : maxFontSize
    $: sizeScale = d3
        //@ts-ignore
        .scaleLinear()
        .domain([0, d3.max(contributions)]);

    $: layout = cloud()
        .size([width, height])
        .padding(5)
        .rotate(() => 0)
        .font("Impact")
        .fontSize((d) => d.size);

    let displayWords: Word[] | null = null;

    let runningLayout = null;

    /**
     * Function that takes concepts, a size, and re-renders until everything fits
     */
    $: startLayout = (concepts, sizeScale, scalePxBy: number = 1) => {
        const fontScale = sizeScale.range([
            scalePxBy * minFontSize,
            scalePxBy * maxPxSize,
        ]);

        const words = concepts.map((c) => {
            return {
                text: c.token,
                size: fontScale(c.contribution),
            } as Word;
        });

        const redefineWords = (newWords: Word[]) => {
            if (newWords.length == words.length) {
                displayWords = newWords;
            } else {
                console.log("Number of cloud words did not align with desired. Rerunning", scalePxBy);
                runningLayout && runningLayout.stop();
                startLayout(concepts, sizeScale, 0.9 * scalePxBy);
            }
        };

        runningLayout = layout
            .words(words)
            .on("end", redefineWords)
            .start();
    };

    $: startLayout(concepts, sizeScale);
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
