<!-- Modified from https://svelte.dev/repl/03f0be0c4dc54eb4af5a168f644f5c31?version=3.19.1 -->

<script>
    import routes from "./navLinks"
</script>

<style lang="postcss">
    a {
        @apply text-xl mx-2 no-underline;
        color: black;
        text-decoration: none;
        border-bottom: none;
    }

    a:hover {
        @apply text-gray-600;
    }
</style>

<nav class="hidden text-gray-500 text-bold sm:block font-semibold">
    {#each routes as route}
        {#if route.newTab}
        <a href={route.url} class="" target="_blank" rel="noopener noreferrer">{route.name}</a>
        {:else}
        <a href={route.url} class="">{route.name}</a>
        {/if}
    {/each}
</nav>