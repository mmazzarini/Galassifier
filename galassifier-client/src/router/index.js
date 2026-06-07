import { createRouter, createWebHistory } from 'vue-router'
import Profile from '../components/Profile.vue'
import GalaxySearch from '../components/GalaxySearch.vue'
import GalaxyResultCard from '../components/GalaxyResultCard.vue'
import EntryForm from '../components/EntryForm.vue'

const routes = [

    {
        path: '/',
        name: 'Home',
        component: EntryForm
    },    
    {
        path: '/profile',
        name: 'Profile',
        component: Profile
    },
    {
        path: '/galaxy-search',
        name: 'GalaxySearch',
        component: GalaxySearch 
    },
    {
        path: '/galaxy-result-card',
        name: 'GalaxyResultCard',
        component: GalaxyResultCard
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router