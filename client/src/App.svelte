<script lang="ts">
	import { onMount } from "svelte";
	import type { Concept } from "./types";
	import WordCloud from "./components/WordCloud.svelte";
	import MemoryGrid from "./components/MemoryGrid.svelte";
	import { API } from "./api";
	import * as _ from "lodash";

	const api = new API();

	let headIndex: number = undefined;
	let conceptList: Concept[] | null = null;
	let memoryGrid: number[][] = undefined;

	function newConcepts(mem: number) {
		// TODO: Debounce this api call
		api.getMemoryConcepts(mem).then((r) => {
			conceptList = r;
		});
	}

	onMount(() => {
		api.getMemoryGrid().then((r) => {
			memoryGrid = r;
		});
	});
</script>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>

<svelte:head>
	<title>FlyBrain Explorer</title>
</svelte:head>

<main>
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
			on:input={_.debounce((e) => newConcepts(+e.target.value), 150)}
			bind:value={headIndex} />
	</div>

	{#if memoryGrid != undefined}
		<MemoryGrid
			cells={memoryGrid}
			on:cellClick={_.debounce((e) => {
				newConcepts(e.detail.cell);
			}, 150)}
			bind:selectedCell={headIndex} />
	{/if}

	{#if conceptList != null}
		<WordCloud concepts={conceptList} />
	{/if}
</main>
