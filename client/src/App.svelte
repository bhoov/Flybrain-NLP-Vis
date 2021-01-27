<script lang="ts">
	import Demo from "./Demo.svelte"
	// import Navbar from "./components/Navbar.svelte"
	import Navbar from './components/Nav/Navbar.svelte'
	import Sidebar from './components/Nav/Sidebar.svelte'

	let open=false;
</script>

<style>
</style>

<Sidebar bind:open/>
<Navbar bind:sidebar={open}/>
<Demo/>

<hr/>