<!-- from https://svelte.dev/repl/03f0be0c4dc54eb4af5a168f644f5c31?version=3.19.1 -->
<script>
	// import Logo from './Logo.svelte'
	import Hamburger from './Hamburger.svelte'
	import Menu from './Menu.svelte'
	
	export let sidebar = false

	let headerClass = "pin"
	let scrollY = 0;
	let lastY = 0;
	let lastDirection = "up";

	function changeClass(y) {
		let result = headerClass;
		const scrolledPxs = lastY - y;
		const scrollDirection = scrolledPxs < 0 ? "down" : "up";
		const changedDirection = scrollDirection !== lastDirection;
		if (changedDirection) {
			result = scrollDirection === "down" ? "unpin" : "pin";
			lastDirection = scrollDirection;
		}
		lastY = y;
		return result;
	}

	$: headerClass = changeClass(scrollY)
</script>

<svelte:window bind:scrollY={scrollY}/>

<style lang="postcss">
	header {
		@apply flex justify-between z-40 bg-gray-300 p-4 items-center text-gray-800 h-8;
	}

	a {
		@apply text-gray-800;
		text-decoration: none;
		border-bottom: 0;
	}
	.fixtop {
		position: fixed;
		left: 0;
		top: 0;
		right: 0;
		z-index: 40;
	}

	.pin {
		top: 0;
	}

	.unpin {
		top: -50px !important;
	}

	.flyvec {
		font-variant: small-caps;
	}

	.smooth {
		transition: 0.4s;
	}
</style>

<div class={`fixtop ${headerClass} smooth`}>
	<header>
		<nav class="flex h-full w-full items-center">
			<div class="md:hidden">
				<Hamburger bind:open={sidebar}/>
			</div>
			<div class="text-3xl font-semibold mx-3 flyvec"><a href="https://arxiv.org/abs/2101.06887" target="_blank">FlyVec</a></div>
		</nav>
	
		<Menu/>
	</header>
</div>