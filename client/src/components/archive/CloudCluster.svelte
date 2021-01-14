<script lang="ts">
    import WordCloud from "./archive/WordCloud.svelte";
    import { api } from "../../api";
    import type * as tp from "../../types";
    import { toggle } from "../../etc/Util";

    export let heads: number[] = [];
    export let cloudWidth: number = 300;
    export let cloudHeight: number = 300;
    export let hoveredHead: number;
    export let selectedHead: number = null;

    function heads2concepts(heads): Promise<tp.Concept[][]> {
        return Promise.all(
            heads.map((h) => {
                return api.getMemoryConcepts(h);
            })
        );
    }

    $: conceptsPromise = heads2concepts(heads);
</script>

<style lang="postcss">
    .status {
        margin: auto;
        color: red;
        vertical-align: middle;
    }

    .cloud {
        border: 1px;
    }

    .hovered {
        @apply text-2xl border-2 border-gray-100;
        transition: font-size 0.1s;
        border: 4px solid cyan;
        border-radius: 1rem;
    }

    .selected {
        box-shadow: 5px 5px 5px 5px coral;
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
        <div
            class:hovered={heads[i] == hoveredHead}
            class:selected={heads[i] == selectedHead}
            class="cloud p-4 my-2 mx-4"
            on:mouseover={() => (hoveredHead = heads[i])}
            on:mouseout={() => (hoveredHead = undefined)}
            on:click={() => (selectedHead = toggle(selectedHead, heads[i]))}
            >
            <WordCloud
                concepts={concept}
                width={cloudWidth}
                height={cloudHeight} />
        </div>
    {/each}
{:catch error}
    <p style="color: red">{error.message}</p>
{/await}
