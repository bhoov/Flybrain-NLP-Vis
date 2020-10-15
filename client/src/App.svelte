<script lang="ts">
	import type {Concept} from "./types"
	import WordCloud from "./components/WordCloud.svelte"
	import {API} from "./api"
	import * as _ from "lodash"

	const api = new API()

	let headIndex: number = undefined;
	let conceptList: Concept[] | null = null

	function inputty(e) {
		let mem = +e.target.value;

		// TODO: Debounce this api call
		api.getMemoryConcepts(mem).then(r => {
			headIndex = mem
			conceptList = r
		})
	}
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

<main>
	<h1>FlyBrain Explorer</h1>
	{#if headIndex != undefined}
		<h3>Showing Concepts for Head {headIndex + 1}</h3>
	{:else}
		<h5>Move the slider to show concepts!</h5>
	{/if}
	<div><input type="range" min="0" max="399" on:input={_.debounce(inputty, 150)} /></div>

	{#if conceptList != null}
		<WordCloud concepts={conceptList}></WordCloud>
	{/if}
</main>
