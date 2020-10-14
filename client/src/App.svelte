<script lang="ts">
	import type {Concept} from "./types"
	import {API} from "./api"

	export let name: string;

	const api = new API()

	let headIndex: number = 1;
	let conceptList: Concept[] | null = null

	function clicky() {
		api.getMemoryConcepts(headIndex).then(r => {
			conceptList = r
		})
	}

	function inputty(e) {
		headIndex = +e.target.value;
		console.log("INPUTTED: ", headIndex);
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
	<h1>Hello {name}!</h1>
	<p>
		Visit the
		<a href="https://svelte.dev/tutorial">Svelte tutorial</a>
		to learn how to build Svelte apps.
	</p>
	<div><input type="range" min="0" max="399" on:input={inputty} /></div>
	<button on:click={clicky}>What concepts for memory {headIndex}?</button>

	{#if conceptList != null}
		<pre>
			{JSON.stringify(conceptList)}
		</pre>
	{/if}
</main>
