<template>
  <div id="default-layout-container">
    <Navigation />
    <nuxt/>
    <Footer />
  </div>
</template>


<script>
import Navigation from '~/components/Navigation'
import Footer from '~/components/Footer'

export default {
	components: {
		Navigation,
		Footer
	}
}
</script>

<style lang='scss'>
@import "~assets/main.scss";
</style>


