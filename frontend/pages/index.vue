<template>
	<div id="index">
		<div class="background-container">
			<div />
		</div>
		<div id="main-container">
			<h1 id="tagline">A diary for the 21st century</h1>

			<img class="screenshot" src="https://fnordserver.eu/images/pageheader/xwordpress-2a9c2494.png.pagespeed.ic.V8x0r10WER.png" />
		</div>
	</div>
</template>

<script>
export default {
	layout: 'no-container',
	auth: 'guest'
}
</script>

<style lang="scss">
#index {
	flex-grow: 1;

	.background-container {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		width: 100%;
		overflow: hidden;
		z-index: -10;

		background-image: linear-gradient(35deg, #036564, #008282);

		>div {
			height: 100vh;
			width: 100%;
			margin-top: -50vh;
			transform: skew(0,-12deg);


			background-image: linear-gradient(35deg,#CDB380 20%,#CDAD80 50%, #CDBA80);
			background-attachment: fixed;
			background-repeat: no-repeat;
			background-size: auto;

		}
	}

	#main-container {
		display: flex;
		flex-direction: column;
		align-items: center;

		#tagline {
			text-align: center;
			font-size: 120px;
			font-weight: 200;
			color: #fff;
			line-height: 1.2;
			text-shadow: 0 -1px 1px #888, 0 1px 1px #FFFFFF;

			margin-bottom: 4rem;
		}

		.screenshot {
			max-height: 70vh;
		}
	}
}
</style>
