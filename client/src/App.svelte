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
		"Senate majority leader discussed the issue with the members of the committee",
		"Entertainment industry shares rise following the premiere of the mass destruction weapon documentary",
		"European Court of Human Rights most compelling cases",
		"White supremacist protest in Washington DC",
		"Apple latest IPhone has an improved apps connectivity",
		"Representative Harris accused Facebook of bias and promoting hate speech",
		"President Trump held campaign rally in Virginia",
		"Stock market plunged on Tuesday following analysts reports",
		"IBM corporation to acquire open-source software startup",
		"Local government officials responded promptly to protests",
		"Influenza vaccine prevented virus outbreak and reduced stress on hospitals",
		"Israeli Palestine confrontation in Gaza",
		"Supreme Court dismissed the criminal charges ",
		"Hillary Clinton declined to comment on the allegations of financial contributions",
		"Research laboratories are working on designing diagnostic tools to assess water contamination using modern AI technologies",
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
			clusterHeads = r.head_info.slice(0, 3).map((c) => c.head);
			$showQueryResults = true;
			keywordifySentence();
		});
		return true;
	}

	$: $queryPhrase && submitPhraseQuery();

	if ($showQueryResults) {
		submitPhraseQuery();
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

		$queryPhrase = interestingExamples[0];

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
	.example-options {
		white-space: pre-wrap;
	}

	.muted {
		@apply text-gray-700;
		opacity: 0.7;
	}

	unmuted {
		opacity: 1 !important;
	}
</style>

<svelte:head>
	<title>Explore Fruit Fly Word Embeddings</title>
</svelte:head>

<main>
	<div class="flex lg:flex-row-reverse flex-wrap">
		<div class="w-full lg:w-2/3 grid grid-cols-2">
			<div id="the-brain" class="self-center">
				{#if memGridOrdering != undefined && activations != undefined}
					<div class="muted mb-2 mx-2">
						All 400
						<a
							href="https://en.wikipedia.org/wiki/Kenyon_cell">Kenyon
							Cells (KCs)</a>
						are represented as a circle in the grid below.
						<strong>Click</strong>
						through each of them to view what concepts each head has
						learned.
					</div>
					<MemoryGrid
						{activations}
						headOrdering={memGridOrdering}
						bind:selectedCell={$headIndex}
						bind:hoveredCell={hoveredHead} />
				{/if}
			</div>
			<div id="concept-exploration" class="my-4">
				{#if conceptList != null}
					<div class="muted">
						Concepts learned by
						<span
							class="font-bold unmuted"
							style="color: coral;">selected KC</span>
					</div>
					<BarChart
						data={conceptList.map((c) => {
							return { name: c.token, value: c.contribution };
						})} />
				{/if}
			</div>
		</div>
		<div id="controls" class="w-full lg:w-1/3 bg-gray-100 rounded-lg px-0">
			<h1>Fruit Fly Word Embeddings</h1>
			<div class="">
				<h4>
					<span class="text-red-700">Search for concepts</span>
					by selecting a phrase dropdown.
				</h4>

				<form>
					<select
						name="example-dropdown"
						class="w-full example-dropdown"
						id="example-dropdown"
						bind:value={$queryPhrase}>
						<!-- on:blur={submitPhraseQuery}> -->
						{#each interestingExamples as ex}
							<option value={ex}>{ex}</option>
						{/each}
					</select>
				</form>

				<div>
					<textarea
						class="w-full h-24 bg-gray-300 cursor-default"
						bind:value={$queryPhrase}
						maxlength="175"
						placeholder="Select a text from the dropdown"
						readonly
						on:keydown={(e) => {
							e.key == 'Enter' && submitPhraseQuery();
							e.code == 'Space' && keywordifySentence();
						}} />
					<!-- <button
						on:click|preventDefault={submitPhraseQuery}
						disabled={$queryPhrase.length < 1}>Query</button> -->
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
		<h1>Top Activated Cells</h1>
		<div class="muted">
			The highest activated KCs from the query phrase. Each KC is
			shown as a bar on the histogram, the height indicating how much the
			selected phrase triggered that particular cell.
		</div>

		<MemoryBars
			barInfo={barInfo.slice(0, 10)}
			bind:hoveredHead
			bind:selectedHead={$headIndex} />

		<div id="query-results" class="grid md:grid-flow-row md:grid-cols-3">
			<CloudCluster
				heads={clusterHeads}
				bind:hoveredHead
				bind:selectedHead={$headIndex} />
		</div>
	{:else}
		<h2 class="text-gray-600 font-thin">
			Query by a keyword phrase above to see what KCs fire the most
		</h2>
	{/if}
</main>
