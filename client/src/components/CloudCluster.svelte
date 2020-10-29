<script lang="ts">
    import WordCloud from "./WordCloud.svelte";
    import { api } from "../api";
    import type * as tp from "../types";

    export let heads: number[] = [];
    export let cloudWidth: number = 300
    export let cloudHeight: number = 300
    export let hoveredHead: number

    function heads2concepts(heads): Promise<tp.Concept[][]> {
        return Promise.all(heads.map(h => {
            return api.getMemoryConcepts(h)
        }))
    }

    $: conceptsPromise = heads2concepts(heads)
</script>

<style lang="postcss">
    .status {
        margin: auto;
        color: red;
        vertical-align: middle
    }

    .hovered {
        @apply text-2xl;
        color: cyan;
        transition: font-size 0.1s;
    }

</style>


{#await conceptsPromise}
    {#if heads.length > 0}
    <div class="status">
        <h1>Loading...</h1>
    </div>
    {/if}
{:then conceptList}
    {#each conceptList as concept, i}
        <div>
            <h2 class:hovered={heads[i] == hoveredHead}>Head {heads[i] + 1}</h2>
            <WordCloud concepts={concept} width={cloudWidth} height={cloudHeight}/>
        </div>
    {/each}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}


