import App from './App.svelte';
import PinnedNeuron from "./components/PinnedNeuron.svelte"

const app = new App({
	target: document.querySelector("#main-demo"),
	props: { }
});

const fig1 = new PinnedNeuron({
	target: document.querySelector("#fig-neuron-disease"),
	props: {
		neuron: 75
	}
})

const fig2 = new PinnedNeuron({
	target: document.querySelector("#fig-neuron-authority"),
	props: {
		neuron: 353
	}
})

export default app;