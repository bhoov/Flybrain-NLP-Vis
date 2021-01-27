<!-- from https://svelte.dev/repl/03f0be0c4dc54eb4af5a168f644f5c31?version=3.19.1 -->
<script>
	// import Logo from './Logo.svelte'
	import Hamburger from './Hamburger.svelte'
	import Menu from './Menu.svelte'
	
	export let sidebar = false
</script>

<header class="flex justify-between bg-gray-200 p-4 items-center text-gray-600 border-b-2 h-8">
	<nav class="flex h-full w-full items-center">
		<div class="md:hidden">
            <Hamburger bind:open={sidebar}/>
        </div>
        <div class="text-3xl font-semibold mx-3">FlyVec</div>
	</nav>
	
	<Menu/>
</header>