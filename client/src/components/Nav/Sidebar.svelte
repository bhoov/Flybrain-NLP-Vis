<!-- from https://svelte.dev/repl/03f0be0c4dc54eb4af5a168f644f5c31?version=3.19.1 -->
<script>
	import routes from "./navLinks"
	export let open = false
</script>

<aside class="absolute w-full h-full bg-gray-200 bg-opacity-20 border-r-2 shadow-lg" class:open>
	<nav class="p-12 text-xl mb-3">
		{#each routes as route}
			<a class="block py-2 my-2 text-2xl" href={route.url}>{route.name}</a>
		{/each}
	</nav>
</aside>

<style>
	aside {
		left: -100%;
		transition: left 0.3s ease-in-out;
		z-index: 10;
	}
	
	.open {
		left: 0
	}
</style>