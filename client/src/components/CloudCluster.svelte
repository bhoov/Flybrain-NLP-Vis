<script lang="ts">
    import WordCloud from "./WordCloud.svelte";
    import { api } from "../api";
    import type * as tp from "../types";

    export let heads: number[] = [];
    export let cloudWidth: number = 300
    export let cloudHeight: number = 300

    function heads2concepts(heads): Promise<tp.Concept[][]> {
        return Promise.all(heads.map(h => {
            return api.getMemoryConcepts(h)
        }))
    }

    $: conceptsPromise = heads2concepts(heads)
</script>

<style>
    .status {
        margin: auto;
        color: red;
        vertical-align: middle
    }

    h3 {
        color: cyan;
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
            <h3>Head {heads[i] + 1}</h3>
            <WordCloud concepts={concept} width={cloudWidth} height={cloudHeight}/>
        </div>
    {/each}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}


