<script>
	import Navbar from './Nav/Navbar.svelte'
	import Sidebar from './Nav/Sidebar.svelte'

	let open=false;
</script>

<Sidebar bind:open/>
<Navbar bind:sidebar={open}/>