<script lang="ts">
    import WordCloud from "./WordCloud.svelte";
    import { api } from "../api";
    import type * as tp from "../types";

    export let heads: number[] [];

    function heads2concepts(heads): Promise<tp.Concept[][]> {
        return Promise.all(heads.map(h => api.getMemoryConcepts(h)))
    }

    $: conceptsPromise = heads2concepts(heads)

    $: console.log("HEADS: ", heads)
    $: console.log("CONEPTS: ", conceptsPromise)

</script>

<style>
    .status {
        margin: auto;
        color: red;
        vertical-align: middle
    }
</style>


{#await conceptsPromise}
    {#if heads.length > 0}
    <div class="status">
        <h1>Loading...</h1>
    </div>
    {/if}
{:then conceptList}
    {#each conceptList as concept, i (heads[i])}
        <div>
            <h2>Head {heads[i]}</h2>
            <WordCloud concepts={concept}/>
        </div>
    {/each}
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}


