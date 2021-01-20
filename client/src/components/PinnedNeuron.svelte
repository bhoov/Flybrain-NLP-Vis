<script lang="ts">
    import {onMount} from "svelte"
    import MemoryGrid from "./MemoryGrid.svelte"
	import BarChart from "./HorizontalBarChart.svelte";
    import {api} from "../api"
    import * as _ from "lodash"
    import * as tp from "../types"

    export let neuron: number

    let neuronLabels: number[]
    let conceptList: tp.Concept[]

    onMount(async () => {
        neuronLabels = await api.getNeuronOrdering()
        conceptList = await api.getNeuronConcepts(neuronLabels[neuron])
    })



</script>

<style>
    .fig {
        border: 2px solid rgba(128, 128, 128, 0.6);
        padding: 0.5rem 0rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
</style>

<div class="fig">
    <div class="text-center font-bold text-2xl">
        {#if neuronLabels}
            Neuron {neuron}
        {:else}
            Neuron ...
        {/if}
    </div>
    
    <div class="grid grid-cols-6">
        <div class="col-start-1 col-end-4 place-self-center">
            {#if neuronLabels}
                <MemoryGrid selectedCell={neuronLabels[neuron]} activations={neuronLabels.map(x => 1)} neuronLabels={neuronLabels} maxOpacity={0.3}/>
            {:else}
                <p>Loading...</p>
            {/if}
        </div>
        <div class="col-start-4 col-end-7">
            {#if conceptList}
                <div class="">
                    <BarChart
                        data={conceptList.map((c) => {
                            return { name: c.token, value: c.contribution };
                        })} />
                </div>
            {:else}
                <p>Loading...</p>
            {/if}
        </div>
    </div>
</div>