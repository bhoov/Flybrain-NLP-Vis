<script lang="ts">
	import { onMount } from "svelte";
	import { headIndex, queryPhrase, showQueryResults } from "./urlStore";
	import type * as tp from "./types";
	// import WordCloud from "./components/WordCloud.svelte";
	// import WordCloud from "./components/WordRanking.svelte";
	import BarChart from "./components/HorizontalBarChart.svelte";
	import MemoryGrid from "./components/MemoryGrid.svelte";
	import CloudCluster from "./components/CloudCluster.svelte";
	import SentenceTokens from "./components/SentenceTokens.svelte";
	import MemoryBars from "./components/MemoryBars.svelte";
	import { api } from "./api";
	import * as _ from "lodash";

	let conceptList: tp.Concept[] | null = null;
	let activations: number[] = undefined;
	let orderedHeads: number[] = undefined;
	let memGridOrdering: number[] = undefined;
	let clusterHeads: number[] | null = null;
	let barInfo: tp.MemActivation[];
	let interestingExamples: string[] = [
		"Israel pakestine conflict",
		"Today I am craving some fried chicken",
	];
	let nHeads: number;
	let keywords: string[] = [];
	let hoveredHead: number;

	function newConcepts(mem: number) {
		api.getMemoryConcepts(mem).then((r) => {
			conceptList = r;
		});
	}

	$: newConcepts($headIndex);

	async function keywordifySentence() {
		keywords = await api.sentenceToKeywords($queryPhrase);
		return true;
	}

	function submitPhraseQuery() {
		api.queryTopMemsByPhrase($queryPhrase).then((r) => {
			activations = r.activations;
			orderedHeads = r.ordered_heads;
			barInfo = r.head_info;
			$headIndex = orderedHeads[0];
			clusterHeads = r.head_info.slice(0, 4).map((c) => c.head);
			$showQueryResults = true
			keywordifySentence();
		});
		return true;
	}


	if ($showQueryResults) {
		submitPhraseQuery()
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

		keywordifySentence();
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
						bind:selectedCell={$headIndex}
						bind:hoveredCell={hoveredHead} />
				{/if}
			</div>
			<div id="concept-exploration" class="">
				{#if conceptList != null}
					<h1>Individual Head Exploration</h1>
					<!-- <WordCloud
						concepts={conceptList}
						width={500}
						height={500} /> -->
					<BarChart
						data={conceptList.map(c => {return {name: c.token, value: c.contribution}})}/>
				{/if}
			</div>
		</div>
		<div id="controls" class="w-full lg:w-1/3 bg-gray-100 rounded-lg">
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
					<textarea
						class="w-full"
						rows="2"
						bind:value={$queryPhrase}
						on:keydown={(e) => {
							e.key == 'Enter' && submitPhraseQuery();
							e.code == 'Space' && keywordifySentence();
						}} />
					<button
						on:click|preventDefault={submitPhraseQuery}
						disabled={$queryPhrase.length < 1}>Query</button>
				</div>

				<div class="flex flex-wrap mb-3 my-4 place-self-start pl-5">
					<span class="mr-2 font-bold border-b-dashed">Detected
						Keywords:
					</span>
					<SentenceTokens tokens={keywords} />
				</div>
			</div>
		</div>
	</div>

	<hr />
	{#if showQueryResults && clusterHeads != null}
		<h2>Query Search Results</h2>

		<MemoryBars barInfo={barInfo.slice(0, 10)} bind:hoveredHead />

		<div
			id="query-results"
			class="grid md:grid-flow-row md:grid-cols-3 overflow-y-auto">
			<CloudCluster heads={clusterHeads} bind:hoveredHead />
		</div>
	{:else}
		<h2 class="text-gray-600 font-thin">
			Query by a keyword phrase above to see what memories fire the most
		</h2>
	{/if}
</main>
