<script lang="ts">
	import { onMount } from "svelte";
	import { headIndex, queryPhrase } from "./urlStore";
	import type * as tp from "./types";
	import WordCloud from "./components/WordCloud.svelte";
	import MemoryGrid from "./components/MemoryGrid.svelte";
	import CloudCluster from "./components/CloudCluster.svelte";
	import SentenceTokens from "./components/SentenceTokens.svelte";
	import { api } from "./api";
	import * as _ from "lodash";

	let conceptList: tp.Concept[] | null = null;
	let activations: number[] = undefined;
	let orderedHeads: number[] = undefined;
	let memGridOrdering: number[] = undefined;
	let clusterHeads: number[] | null = null;
	let interestingExamples: string[] = [
		"Israel pakestine conflict",
		"Today I am craving some fried chicken",
	];
	let nHeads: number;
	let tokens: string[] = []

	function newConcepts(mem: number) {
		api.getMemoryConcepts(mem).then((r) => {
			conceptList = r;
		});
	}

	$: newConcepts($headIndex);

	async function tokenizeSentence() {
		tokens = await api.sentenceToTokens($queryPhrase)
	}

	function submitPhraseQuery() {
		api.queryTopMemsByPhrase($queryPhrase).then((r) => {
			activations = r.activations;
			console.log("Activations: ", activations);
			orderedHeads = r.ordered_heads;
			$headIndex = orderedHeads[0];
			clusterHeads = r.head_info.slice(0, 4).map((c) => c.head);
		});
	}

	onMount(() => {
		api.getNHeads().then((H) => {
			nHeads = H;
			activations = _.range(H).map((v) => 1);

			api.getMemoryOrder().then((r) => {
				memGridOrdering = r;
				console.log("Mem grid ordering: ", memGridOrdering);
			});
		});

		tokenizeSentence()
	});
</script>

<style global lang="postcss">
	@tailwind base;
	h1 {
		@apply text-3xl font-bold;
	}
	h2 {
		@apply text-xl;
	}
	h3 {
		@apply text-lg;
	}
	a {
		@apply text-blue-600 underline;
	}
	@tailwind components;
	@tailwind utilities;
	main {
		text-align: center;
		padding: 1em;
		margin: auto;
		max-width: 1200px;
	}

	#query-results {
		max-height: 350px;
	}
</style>

<svelte:head>
	<title>FlyBrain Explorer</title>
</svelte:head>

<main>
	<div class="flex lg:flex-row-reverse flex-wrap">
		<div class="w-full lg:w-2/3 grid grid-cols-2">
			<div id="the-brain" class="self-center">
				{#if memGridOrdering != undefined && activations != undefined}
					<MemoryGrid
						{activations}
						headOrdering={memGridOrdering}
						bind:selectedCell={$headIndex} />
				{/if}
			</div>
			<div id="concept-exploration" class="">
				{#if conceptList != null}
					<h2>Individual Head Exploration</h2>
					<WordCloud
						concepts={conceptList}
						width={400}
						height={400} />
				{/if}
			</div>
		</div>
		<div id="controls" class="w-full lg:w-1/3">
			<h1>FlyBrain Explorer</h1>
			<div class="">
				{#if $headIndex != undefined}
					<h3>
						Showing Concepts for Head
						<input
							type="number"
							min="1"
							max={nHeads}
							value={$headIndex + 1}
							on:input={(e) => {
								//@ts-ignore
								const val = e.target.value - 1;
								$headIndex = val > nHeads - 1 ? nHeads - 1 : val < 0 ? 0 : val;
							}} />
					</h3>
				{/if}

				<h4>
					Or,
					<span class="text-red-700">search for concepts</span>
					by typing in a phrase below or selecting from the dropdown:
				</h4>

				<form>
					<select
						name="example-dropdown"
						bind:value={$queryPhrase}
						on:input={submitPhraseQuery}>
						{#each interestingExamples as ex}
							<option value={ex}>{ex}</option>
						{/each}
					</select>
				</form>

				<div>
					<input
						type="text"
						bind:value={$queryPhrase}
						on:keydown={(e) => {
							e.key == 'Enter' && submitPhraseQuery();
						}} />
					<button
						on:click|preventDefault={submitPhraseQuery}
						disabled={$queryPhrase.length < 1}>Query</button>
				</div>

				<div class="flex flex-wrap mb-3 my-4 place-self-start pl-5">
					<span class="mr-2 font-bold">Tokens: </span>
					<SentenceTokens {tokens} />
				</div>
			</div>
		</div>
	</div>

	<hr />
	{#if clusterHeads != null}
		<h2>Query Search Results</h2>

		<div
			id="query-results"
			class="grid md:grid-flow-row md:grid-cols-3 overflow-y-auto">
			<CloudCluster heads={clusterHeads} />
		</div>
	{:else}
		<h2 class="text-gray-600 font-thin">
			Query by a keyword phrase above to see what memories fire the most
		</h2>
	{/if}
</main>
