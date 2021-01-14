<script lang="ts">
    import FetchWordCloud from "./FetchWordCloud.svelte";
    import { toggle } from "../etc/Util";

    export let heads: number[] = [];
    export let importances: number[] = [];
    export let cloudWidth: number = 250;
    export let cloudHeight: number = 250;
    export let hoveredHead: number;
    export let selectedHead: number = null;
</script>

<style lang="postcss">
    .status {
        margin: auto;
        color: red;
        vertical-align: middle;
    }

    .cloud {
        border: 4px solid #3c3c3c3c;
        border-radius: 3px;
        margin: 0 1rem;
    }

    .hovered {
        transition: font-size 0.1s;
        border-color: cyan;
    }

    .selected {
        box-shadow: 5px 5px 5px 5px coral;
    }
</style>

{#each heads as head, i}
        <div
            class:hovered={head == hoveredHead}
            class:selected={head == selectedHead}
            class="cloud border-2 border-gray-800"
            on:mouseover={() => (hoveredHead = head)}
            on:mouseout={() => (hoveredHead = undefined)}
            on:click={() => (selectedHead = toggle(selectedHead, head))}
            >
            <FetchWordCloud
                unit={head}
                {importances}
                currIdx={i}
                width={cloudWidth}
                height={cloudHeight} />
        </div>
{/each}
