<template>
  <div id="default-layout-container">
    <Navigation />
    <div id="main-container">
      <nuxt/>
    </div>
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


