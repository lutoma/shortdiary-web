<template>
	<RouterView v-slot="{ Component }">
		<transition name="login-anim">
			<component :is="Component" />
		</transition>
	</RouterView>
</template>

<style lang='scss'>
//@use "@/assets/main.scss" as *;

.login-anim-enter-active, .login-anim-leave-active {
	position: absolute;
	max-height: 100%;
	top: 0px;
	left: 0px;
}

.login-anim-leave-active {
	transition: max-height 0.25s cubic-bezier(1, 0.5, 0.8, 1);

	> div {
		transition: opacity 0.15s cubic-bezier(1, 0.5, 0.8, 1);
	}
}

.login-anim-enter-from, .login-anim-leave-to {
	max-height: 0px;

	> div {
		opacity: 0;
	}
}
</style>
