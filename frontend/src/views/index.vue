<template>
	<div id="index">
		<div class="background-container">
			<video autoplay loop>
				<source src="~assets/frontpage-video/background_av1.mp4" type="video/mp4">
				<source src="~assets/frontpage-video/background.mp4" type="video/mp4">
				<source src="~assets/frontpage-video/background.webm" type="video/webm">
			</video>
		</div>
		<div id="main-container">
			<h1 id="tagline">A diary for the 21st century</h1>
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
		height: 100vh;
		width: 100vw;
		overflow: hidden;
		z-index: -10;
		pointer-events: none;

		video {
			min-width: 100vw;
			min-height: 100vh;
		}
	}

	#main-container {
		display: flex;
		flex-direction: column;
		align-items: center;

		#tagline {
			text-align: center;
			font-size: 120px;
			//font-weight: 200;
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
