<script>
    let authors = [
					{
						"author":"Benjamin Hoover",
						"authorURL":"https://bhoov.com",
						"affiliations": [{"name": "IBM Research", "url": "https://www.draco.res.ibm.com/"}]
					},
					{
						"author":"Yuchen Liang",
						"authorURL":"https://airc.rpi.edu/people/staff/yuchen-liang",
						"affiliations": [
							{"name": "RPI", "url": "https://science.rpi.edu/computer-science"},
							{"name": "MIT-IBM Watson AI Lab", "url": "https://mitibmwatsonailab.mit.edu/"}
						]
					},
					{
						"author":"Chaitanya K. Ryali",
						"authorURL":"https://scholar.google.com/citations?user=4LWx24UAAAAJ&hl=en",
						"affiliations": [{"name": "UC San Diego", "url": "https://cse.ucsd.edu/"}]
					},
					{
						"author":"Leopold Grinberg",
						"authorURL":"http://www.dam.brown.edu/people/lgrinb/",
						"affiliations": [{"name": "IBM Research", "url": "https://www.draco.res.ibm.com/"}]
					},
					{
						"author":"Hendrik Strobelt",
						"authorURL":"http://hendrik.strobelt.com/",
						"affiliations": [
							{"name": "MIT-IBM Watson AI Lab", "url": "https://mitibmwatsonailab.mit.edu/"},
							{"name": "IBM Research", "url": "https://www.draco.res.ibm.com/"}
						]
					},
					{
						"author":"Saket Navlakha",
						"authorURL":"https://navlakhalab.net/",
						"affiliations": [{"name": "Cold Spring Harbor Laboratory", "url": "https://www.cshl.edu/"}]
					},
					{
						"author":"Mohammed J. Zaki",
						"authorURL":"http://www.cs.rpi.edu/~zaki/",
						"affiliations": [{"name": "RPI", "url": "https://science.rpi.edu/computer-science"}]
					},
					{
						"author":"Dmitry Krotov",
						"authorURL":"https://mitibmwatsonailab.mit.edu/people/dmitry-krotov/",
						"affiliations": [
							{"name": "MIT-IBM Watson AI Lab", "url": "https://mitibmwatsonailab.mit.edu/"},
							{"name": "IBM Research", "url": "https://www.draco.res.ibm.com/"}
						]
					}
				]
</script>

<style lang="postcss">
    .col-title {
        @apply uppercase text-gray-500 text-xs;
    }

    .left-col {
        @apply col-start-1 col-end-6;
    }

    .right-col {
        @apply col-start-6 col-end-13;
    }

    @screen lg {
        .left-col {
            @apply col-start-2;
        }

        .right-col {
            @apply col-start-7;
        }
    }

    a {
        @apply text-blue-700;
        border-bottom: none;
    }

    .author {
        @apply font-semibold;
    }
</style>

<div class="grid gap-x-3 grid-cols-12 text-sm">
        <div class="col-title left-col">Authors</div>
        <div class="col-title right-col">Affiliations</div>
        {#each authors as author}
            <div class="author left-col">
                <div>
                    <a href={author.authorURL} target="_blank" class="author">{author.author}</a>
                </div>
            </div>
            <div class="affiliation right-col">
                <div>
                    {#each author.affiliations as aff, i}
                        <a href={aff.url} target="_blank" class="affiliation">{aff.name}</a>{#if i != (author.affiliations.length - 1)}<span class="mr-1">, </span>{/if}
                    {/each}
                </div>
            </div>
        {/each}
</div>