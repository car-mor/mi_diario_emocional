<template>
  <div class="flex h-screen">
    <Sidebar />
    <Streak :count="12" />
    <PageTitle title="Recursos de autoayuda" />


    <main class="flex-1 p-6 overflow-y-auto">
      <router-view />
    </main>

    <UserProfile />
  </div>
</template>

<script setup lang="ts">
import Sidebar from "../components/SidebarPatient.vue"
import Streak from "../components/StreakPatient.vue"
import PageTitle from "../components/PatientPageTitle.vue"


//import UserProfile from "/components/UserProfile.vue"
</script>
