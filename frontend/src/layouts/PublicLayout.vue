<template>
	<div id="public-layout-container">
		<div>
			<h1 class="brand">
				shortdiary
			</h1>
			<el-card>
				<RouterView />
			</el-card>
			<footer>
				<ul>
					<li><a rel="noopener" target="_blank" href="https://github.com/lutoma/shortdiary">Source code</a></li>
					<li><a rel="noopener" target="_blank" href="https://fnordserver.eu/en/privacy-policy">Privacy</a></li>
					<li><a rel="noopener" target="_blank" href="https://fnordserver.eu/en/imprint">Legal notice</a></li>
					<li><a rel="noopener" target="_blank" href="https://fnordserver.eu/en/contact">Contact</a></li>
				</ul>
			</footer>
		</div>
	</div>
</template>

<script setup>
</script>

<style lang='scss'>
@use "@/assets/main.scss" as *;

#public-layout-container {
	// Needed for login animation to make sure this stays above el-card
	// elements in dashboard
	z-index: 10000;

	background: #036564;

	width: 100%;
	height: 100%;

	display: flex;
	justify-content: center;
	padding-top: 8rem;

	> div {
		display: flex;
		flex-direction: column;
		align-items: center;

		> .brand {
			color: #fff;
		}

		> .el-card {
			width: 400px;
			max-width: 90vw;

			text-align: center;
			padding-top: 1rem;
			//padding: 2.5rem 3rem;
		}

		> footer {
			margin-top: 1rem;
			font-size: 12px;
			user-select: none;

			ul {
				list-style-type: none;
				padding: 0;

				li {
					display: inline;
					margin: 0;
					margin-right: 1rem;
				}

				a {
					color: white;
				}
			}
		}
	}
}
</style>
