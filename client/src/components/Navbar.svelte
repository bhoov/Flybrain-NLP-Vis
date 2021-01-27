<script>
    let routes = [
        {
            name: "Blog",
            url: "#blog-title"
        }
    ]
</script>
<div class="w-full h-10 bg-blue-300 z-30">
    <div class="text-lg font-extrabold content-center flex my-auto h-full mx-6">
        {#each routes as route}
        <a href={route.url}>{route.name}</a>
        {/each}
    </div>
</div>

