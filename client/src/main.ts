import App from './App.svelte';
import PinnedNeuron from "./components/PinnedNeuron.svelte"
import FetchCloudCluster from "./components/FetchCloudCluster.svelte"
import {offensiveNeurons} from "./store"
import * as api from "./api"

const app = new App({
	target: document.querySelector("#main-demo"),
	props: { }
});

const fig1 = new PinnedNeuron({
	target: document.querySelector("#fig-neuron-disease"),
	props: {
		neuron: 75,
		offensiveNeurons
	}
})

const fig2 = new PinnedNeuron({
	target: document.querySelector("#fig-neuron-authority"),
	props: {
		neuron: 353,
		offensiveNeurons
	}
})

const exampleSentence = "Entertainment industry shares rise following the premiere of the mass destruction weapon documentary." // Make this static?
const result = {
	heads: [142, 388, 78, 113],
	importances: [
		0.08464591562947799,
		0.008717435018951041,
		0.0037374164217366676,
		0.003055522026112061
	],
	labels: [195, 189, 280, 313],
	offensiveNeurons: new Set([87, 96, 138, 153, 358])
}


const fig3 = new FetchCloudCluster({
	target: document.querySelector("#fig-entertainment-cloud"),
	props: {...result, mouseable: false},
})

export default app;