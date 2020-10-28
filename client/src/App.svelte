<script lang="ts">
	import { onMount } from "svelte";
	import type * as tp from "./types";
	import WordCloud from "./components/WordCloud.svelte";
	import MemoryGrid from "./components/MemoryGrid.svelte";
	import CloudCluster from "./components/CloudCluster.svelte";
	import { api } from "./api";
	import * as _ from "lodash";

	let headIndex: number = 0;
	let conceptList: tp.Concept[] | null = null;
	let activations: number[] = undefined;
	let orderedHeads: number[] = undefined;
	let memGridOrdering: number[] = undefined;
	let queryPhrase: string = "";
	let clusterHeads: number[] | null = null;

	function newConcepts(mem: number) {
		api.getMemoryConcepts(mem).then((r) => {
			conceptList = r;
		});
	}

	$: newConcepts(headIndex);

	function submitPhraseQuery() {
		api.queryTopMemsByPhrase(queryPhrase).then((r) => {
			activations = r.activations;
			console.log("Activations: ", activations);
			orderedHeads = r.ordered_heads;
			headIndex = orderedHeads[0];
			clusterHeads = r.head_info.slice(0, 4).map((c) => c.head);
		});
	}

	onMount(() => {
		api.getNHeads().then((r) => {
			activations = _.range(r).map((v) => 1);

			api.getMemoryOrder().then((r) => {
				memGridOrdering = r;
				console.log("Mem grid ordering: ", memGridOrdering);
			});
		});
	});
</script>

<style>
	main {
		text-align: center;
		padding: 1em;
		margin: auto;
		display: grid;
		grid-template-columns: auto 500px auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 300;
	}

	h2 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 2em;
		font-weight: 100;
	}

	@media (min-width: 768px) {
		main {
			display: grid;
			grid-template-columns: minmax(30%, auto) 30% minmax(30%, auto);
			margin: 0, auto;
		}
	}
</style>

<svelte:head>
	<title>FlyBrain Explorer</title>
</svelte:head>

<main>
	<div class="left">
		{#if conceptList != null}
			<h2>Individual Head Exploration</h2>
			<WordCloud concepts={conceptList} width={400} height={400} />
		{/if}
	</div>
	<div class="center">
		<h1>FlyBrain Explorer</h1>
		{#if headIndex != undefined}
			<h3>Showing Concepts for Head {headIndex + 1}</h3>
		{:else}
			<h4>Move the slider or click a cell to show concepts!</h4>
		{/if}
		<div>
			<input
				type="range"
				min="0"
				max="399"
				bind:value={headIndex} />
		</div>

		<h4>Or, search for concepts by typing in a phrase below:</h4>

		<div>
			<input type="text" bind:value={queryPhrase} />
			<button
				on:click={submitPhraseQuery}
				disabled={queryPhrase.length < 1}>Query</button>
		</div>
		{#if memGridOrdering != undefined && activations != undefined}
			<MemoryGrid
				{activations}
				headOrdering={memGridOrdering}
				bind:selectedCell={headIndex} />
		{/if}
	</div>

	<div class="right">
		{#if clusterHeads != null}
			<h2>Query Search Results</h2>
			<CloudCluster heads={clusterHeads} />
		{/if}
	</div>
</main>
