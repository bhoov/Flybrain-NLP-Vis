<script lang="ts">
    import {onMount} from "svelte"
    import MemoryGrid from "./MemoryGrid.svelte"
	import BarChart from "./HorizontalBarChart.svelte";
    import {api} from "../api"
    import * as _ from "lodash"
    import * as tp from "../types"

    export let neuron: number
    export let offensiveNeurons: Set<number>

    let neuronLabels: number[]
    let conceptList: tp.Concept[]
    let selectedCell

    onMount(async () => {
        neuronLabels = await api.getNeuronOrdering()
        selectedCell = neuronLabels[neuron]
        conceptList = await api.getNeuronConcepts(selectedCell)
    })

    $: {
        api.getNeuronConcepts(selectedCell).then(r => {
            conceptList = r
        })
    }

    $: barchartData = conceptList?.map(c => {
        return { name: c.token, value: c.contribution };
    })


</script>

<style>
    .fig {
        border: 2px solid rgba(128, 128, 128, 0.6);
        padding: 0.5rem 0rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        min-height: 280px;
        max-height: 380px;
    }
</style>

<div class="fig">
    <div class="text-center font-bold text-2xl">
        Neuron {neuron}
    </div>
    
    <div class="flex justify-between h-full items-center">
        <div class="px-3 flex-1">
            {#if neuronLabels}
                <MemoryGrid bind:selectedCell={selectedCell} activations={neuronLabels.map(x => 1)} {offensiveNeurons} neuronLabels={neuronLabels} maxOpacity={0.3} allowInteraction={false}/>
            {:else}
                <p>Loading...</p>
            {/if}
        </div>
        <div class="flex-1">
            {#if barchartData}
                <div class="">
                    <BarChart data={barchartData} />
                </div>
            {:else}
                <p>Loading...</p>
            {/if}
        </div>
    </div>
</div>