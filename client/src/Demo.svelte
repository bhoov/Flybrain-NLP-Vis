
<script lang="ts">
	import { onMount } from "svelte";
	import {
		neuronIndex,
		queryPhrase,
		showQueryResults,
		allowCustomInput,
		offensiveNeurons
	} from "./store";
	import type * as tp from "./types";
	import Select from "svelte-select";
	import Navbar from "./components/Navbar.svelte";
	import BarChart from "./components/HorizontalBarChart.svelte";
	import MemoryGrid from "./components/MemoryGrid.svelte";
	import FetchCloudCluster from "./components/FetchCloudCluster.svelte";
	import FetchWordCloud from "./components/FetchWordCloud.svelte";
	import SentenceTokens from "./components/SentenceTokens.svelte";
	import { api } from "./api";
	import * as _ from "lodash";

	let conceptList: tp.Concept[] | null = null; // Tokens and contributions for the selected neuron
	let activations: number[] = undefined; // How much each neuron was activated by the query
	let loadingActivations: boolean = false; // Are we waiting for real activations?
	let neuronGridOrdering: number[] = undefined; // What order to display the neurons on the grid
	let topNeuronClusters: number[] | null = null; // Cloud clusters to show
	let clusterImportance: number[] | null = null; // Activations corresponding to topNeuronClusters
	let searchResultHeight = 250; // How high to make the search result grid
	let kNearest = 4; // Number of nearest cluster clouds to show
	let interestingExamples: string[] = [
		// Default examples for selection
		"Senate majority leader discussed the issue with the members of the committee",
		"Entertainment industry shares rise following the premiere of the mass destruction weapon documentary",
		"European Court of Human Rights most compelling cases",
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
	$: selectExamples = interestingExamples.map((s) => {
		return {
			value: s,
			label: s,
		};
	});
	let keywords: string[] = []; // Extracted keywords from the query
	let hoveredNeuronIdx: number;

	/**
	 * Convert a neuron to its learned concepts
	 * @param neuron -- Neuron index to search for
	 */
	function newConcepts(neuron: number) {
		api.getNeuronConcepts(neuron).then((r) => {
			conceptList = r;
		});
	}

	$: getLabel = (idx: number) => {
		return neuronGridOrdering ? _.findIndex(neuronGridOrdering, (v) => v == idx) : idx
	}

	$: newConcepts($neuronIndex);

	/**
	 * Extract keywords from a provided sentence
	 */
	async function keywordifySentence() {
		keywords = await api.sentenceToKeywords($queryPhrase);
		return keywords.length > 0;
	}

	/**
	 * Submit the phrase as a query
	 */
	function submitPhraseQuery() {
		api.queryTopNeuronsByPhrase($queryPhrase).then((r) => {
			activations = r.activations;
			loadingActivations = false;
			topNeuronClusters = r.head_info
				.slice(0, kNearest)
				.map((c) => c.head);
			clusterImportance = r.head_info
				.slice(0, kNearest)
				.map((c) => c.activation);
			$showQueryResults = true;
			keywordifySentence();
		});
		return true;
	}

	$: topNeuronLabels = topNeuronClusters?.map(getLabel);
	/**
	 * Get phrase query from event
	 */
	function handleQuery(event) {
		console.log("EVENT ", event);
		$queryPhrase = event.detail.value;
	}

	// Whenever the query phrase changes, resubmit query
	$: $queryPhrase && submitPhraseQuery();

	if ($showQueryResults) {
		submitPhraseQuery();
	}

	onMount(() => {
		api.getNNeurons().then((H) => {
			// Give all activations a default coloring
			activations = _.range(H).map((v) => 0.5);
			loadingActivations = true;
			submitPhraseQuery();

			api.getNeuronOrdering().then((r) => {
				neuronGridOrdering = r;
			});
		});

		$queryPhrase = interestingExamples[0];

		keywordifySentence();
	});
</script>

<style global lang="postcss">
	@tailwind base;
	@tailwind components;
	@tailwind utilities;

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
		@apply underline;
	}
	main {
		/* text-align: center; */
		margin: auto;
		max-width: 1560px;
	}

	.muted {
		@apply text-gray-700;
		opacity: 0.7;
	}

	.unmuted {
		opacity: 1 !important;
	}

	.em {
		@apply text-red-700;
	}

	.action {
		@apply font-extrabold;
	}


	/* Demo layout wrappers */
	.main {
		@apply col-start-3 col-end-11;
	}

	.left-comment {
		@apply col-start-1 col-end-3 align-middle muted font-semibold my-2;
	}

	.right-comment {
		@apply col-start-11 col-end-13 muted font-semibold my-2 place-self-center align-middle;
	}

	.example-options {
		white-space: pre-wrap;
	}

	.max-cell {
		max-width: 300px;
		max-height: 300px;
	}

	.em-fly {
		@apply text-blue-500 font-semibold;

	}
	.fly-perspective {
		@apply font-thin;
	}
</style>

<svelte:head>
	<title>Explore Fruit Fly Word Embeddings</title>
	<link rel="stylesheet" href="https://unpkg.com/tippy.js/dist/tippy.css" />
</svelte:head>

<main class="lg:grid lg:grid-cols-12 lg:gap-4 px-4">
	<div id="demo-title" class="w-full leading-normal text-center text-5xl font-bold my-3 main">
		Fruit Fly Word Embeddings
	</div>
	<div class="left-comment">
		<div>
			<span class="em">Select a query phrase</span> from the dropdown {#if $allowCustomInput}<span>or type in your own sentence</span>{/if} 
			to search for most related concepts
		</div>
		<div class="fly-perspective mt-3">
			This sentence corresponds to providing our fly-inspired model a <span class="em-fly">smell</span> or analogous sensory input. 
			The displayed wordclouds represent the <a href="http://www.scholarpedia.org/article/Receptive_field">receptive fields</a> of the top activated 
			<a href="https://en.wikipedia.org/wiki/Kenyon_cell"><span class="em-fly">Kenyon Cells</span></a> (KCs).
		</div>
	</div>
	<div class="w-full main">
		<div class="w-full bg-gray-100 rounded-lg px-0">
			<div>
				<Select
					items={selectExamples}
					selectedValue={selectExamples[0]}
					hideEmptyState={$allowCustomInput}
					isCreatable={$allowCustomInput}
					placeholder={'Select from the suggested' + ($allowCustomInput ? 'OR type your own short phrase' : '')}
					getOptionLabel={(option, filterText) => {
						return option.isCreator ? filterText : option.label;
					}}
					on:select={handleQuery} />
				<div
					class="flex flex-wrap mb-3 my-2 place-self-start pl-5 content-center">
					<div class="mr-2 font-bold border-b-dashed align-middle">
						Detected Keywords:
					</div>
					<SentenceTokens tokens={keywords} />
				</div>
			</div>
		</div>
		<div class="top-results">
			{#if showQueryResults && topNeuronClusters != null}
				<!-- <div class="muted">
							The highest activated KCs from the query phrase. Each KC is
							shown as a bar on the histogram, the height indicating how much
							the selected phrase triggered that particular cell.
						</div> -->
				<div id="query-results"
						class="sm:grid sm:grid-cols-2 lg:grid-flow-row lg:grid-cols-4 gap-x-0.5 place-items-center">
						<FetchCloudCluster
							heads={topNeuronClusters}
							labels={topNeuronLabels}
							{offensiveNeurons}
							importances={clusterImportance}
							bind:hoveredHead={hoveredNeuronIdx}
							bind:selectedHead={$neuronIndex} />
					</div>
			{:else}
				<h2
					class="text-gray-600 font-thin align-middle"
					style={`height: ${searchResultHeight}`}>
					Query by a keyword phrase above to see what KCs fire the most
				</h2>
			{/if}
			<hr />
		</div>
	</div>
	<div class="left-comment">
		<div>
			<span class="action">Click</span> and <span class="action">hover</span> over the grid to <span class="em">explore every concept</span>
			learned by our model
		</div>
		<div class="my-4 fly-perspective">
			Each circle on the grid represents a KC with its corresponding receptive field (optimal stimulus that leads to the KC’s activation).
		</div>
	</div>
	<div class="explorer lg:grid lg:grid-cols-3 gap-6 main place-items-center">
		<div id="the-brain" class="justify-self-center">
			{#if neuronGridOrdering != undefined && activations != undefined}
				<div class="w-full text-center max-cell">
					<MemoryGrid
						{activations}
						loading={loadingActivations}
						neuronLabels={neuronGridOrdering}
						{offensiveNeurons}
						bind:selectedCell={$neuronIndex}
						bind:hoveredCell={hoveredNeuronIdx} />
				</div>
			{/if}
		</div>
		<div id="concept-exploration" class="my-4 justify-self-center max-cell">
			{#if conceptList != null && !offensiveNeurons.has(getLabel($neuronIndex))}
				<div class="muted">
					Concepts learned by
					<span
						class="font-bold unmuted"
						style="color: coral;">Neuron {getLabel($neuronIndex)}</span>
				</div>
				<div class="max-cell">
					<BarChart
						data={conceptList.map((c) => {
							return { name: c.token, value: c.contribution };
						})} />
				</div>
			{/if}
		</div>
		<div class="hidden lg:block place-self-center w-full max-cell">
			<FetchWordCloud
				unit={$neuronIndex}
				label={getLabel($neuronIndex)}
				hideContent={offensiveNeurons.has(getLabel($neuronIndex))}
				selected={true} />
		</div>
	</div>
		<div class="right-comment">
			<a href="#blog-title" class="no-underline text-center muted">
				<div class="text-xl my-4">See blog post below </div>
				<div class="text-center"><i class="fas fa-angle-double-down fa-3x"></i></div>
			</a>
		</div>
</main>