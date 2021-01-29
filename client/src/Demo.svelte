
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
	import interestingExamples from "./config/exampleSentences"
	import api from "./staticApi";
	import * as _ from "lodash";

	let conceptList: tp.Concept[] | null = null; // Tokens and contributions for the selected neuron
	let activations: number[] = undefined; // How much each neuron was activated by the query
	let loadingActivations: boolean = false; // Are we waiting for real activations?
	let neuronGridOrdering: number[] = undefined; // What order to display the neurons on the grid
	let topNeuronClusters: number[] | null = null; // Cloud clusters to show
	let clusterImportance: number[] | null = null; // Activations corresponding to topNeuronClusters
	let searchResultHeight = 250; // How high to make the search result grid
	let kNearest = 4; // Number of nearest cluster clouds to show
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

	:root {
		--selected: coral;
		--hovered: cyan;
		--emphasized: theme("colors.red.600");
	}

	.selected {
		color: var(--selected);
	}

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
		margin: auto;
		max-width: 1560px;
		padding-top: 3rem;
	}

	.muted {
		@apply text-gray-700;
		opacity: 0.7;
	}

	.unmuted {
		opacity: 1 !important;
	}

	.em {
		color: var(--emphasized);
	}

	.action {
		@apply font-extrabold;
	}


	/* Demo layout wrappers */
	.main {
		@apply col-start-3 col-end-11;
	}

	.left-comment {
		@apply col-start-1 col-end-3 align-middle font-semibold my-2;
	}

	.right-comment {
		@apply col-start-11 col-end-13 muted font-semibold my-2 place-self-center align-middle;
	}

	.example-options {
		white-space: pre-wrap;
	}

	.max-cell {
		width: 300px;
		height: 300px;
		margin-bottom: 0.75rem;
	}

	.em-fly {
		@apply text-blue-500 font-semibold;
	}

	.fly-perspective {
		@apply font-thin;
	}

	.explorer {
		min-height: 300px;
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
			<span class="em">Select a query phrase</span>
				<span class="muted">
					from the dropdown {#if $allowCustomInput}or type in your own sentence{/if}
					to search for most related concepts
				</span>
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
						class="gap-x-0.5 sm:grid sm:grid-cols-2 lg:grid-flow-row lg:grid-cols-4 lg:gap-x-1 place-items-center">
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
			<span class="muted"><span class="action">Click</span> and <span class="action">hover</span> over the grid to</span> <span class="em">explore every concept</span>
			<span class="muted">learned by our model</span>
		</div>
		<div class="my-4 fly-perspective">
			Each circle on the grid represents a KC with its corresponding receptive field (optimal stimulus that leads to the KC’s activation).
		</div>
	</div>


	<div class="explorer main flex flex-wrap justify-between items-center mb-4">
		<div id="the-brain" class="max-cell">
			{#if neuronGridOrdering != undefined && activations != undefined}
				<div class="w-full text-center">
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
		<div id="concept-exploration" class="max-cell flex-none">
			{#if conceptList != null && !offensiveNeurons.has(getLabel($neuronIndex))}
				<div class="muted text-center">
					Concepts learned by
					<span
						class="font-bold unmuted selected">Neuron {getLabel($neuronIndex)}</span>
				</div>
				<div class="max-cell">
					<BarChart
						data={conceptList.map((c) => {
							return { name: c.token, value: c.contribution };
						})} />
				</div>
			{/if}
		</div>
		<div class="hidden lg:block w-full max-cell flex-none">
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