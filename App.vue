<template>
  <div>
    <!-- Only show navigation when NOT on landing page -->
    <nav v-if="!isLandingPage" class="navbar">
      <div class="logo-container">
        <img src="/logo.png" alt="Logo" class="logo" />
      </div>

      <div class="nav-links">
        <router-link to="/home" class="nav-link">Home</router-link>
        <router-link to="/input" class="nav-link">Input</router-link>
        <router-link to="/history" class="nav-link">History</router-link>
        <router-link to="/analytics" class="nav-link">Analytics</router-link>
      </div>
    </nav>

    <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    isLandingPage() {
      return this.$route.path === '/';
    }
  }
}
</script>

<style>
/* Google modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;

  /* Transparent modern green */
background: linear-gradient(135deg, rgba(197, 26, 26, 0.8) 0%, rgba(5, 43, 1, 0.8) 100%);
  backdrop-filter: blur(10px);

  padding: 10px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;

  border-bottom: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);

  font-family: 'Inter', sans-serif;
}

.logo {
  height: 60px;
  filter: drop-shadow(0 0 4px rgba(0,0,0,0.4));
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  gap: 26px;
}

.nav-link {
  color: white;
  font-size: 15.5px;
  font-weight: 500;
  letter-spacing: 0.4px;
  text-decoration: none;

  position: relative;
  padding: 6px 0;

  transition: color 0.3s ease;
}

/* Modern underline animation */
.nav-link::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0%;
  height: 2px;
  background: white;
  border-radius: 3px;

  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

/* Active route underline */
.nav-link.router-link-active::after {
  width: 100%;
}
/* Keep underline when the link is active */
.nav-link.router-link-active::after,
.nav-link.router-link-exact-active::after {
  width: 100%;
}
</style>