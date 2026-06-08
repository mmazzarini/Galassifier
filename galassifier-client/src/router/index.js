import { createRouter, createWebHistory } from 'vue-router'
import GalaxySearch from '../components/GalaxySearch.vue'
import GalaxyResultCard from '../components/GalaxyResultCard.vue'
import EntryPage from '../components/EntryPage.vue'


const routes = [

    {
        path: '/',
        name: 'Home',
        component: EntryPage
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
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router