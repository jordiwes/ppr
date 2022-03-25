// Libraries
import Vue from 'vue'
import Vuetify from 'vuetify'
import { getVuexStore } from '@/store'
import CompositionApi from '@vue/composition-api'
import { mount, createLocalVue, Wrapper } from '@vue/test-utils'
import { mockFlags, ldClientMock, resetLDMocks } from 'jest-launchdarkly-mock'

// Components
import SearchBarList from '@/components/search/SearchBarList.vue'

// Other
import { MHRSearchTypes, SearchTypes } from '@/resources'
import {
  mockedDisableAllUserSettingsResponse
} from './test-data'
import { UISearchTypes } from '@/enums'
import { getLastEvent } from './utils'
import flushPromises from 'flush-promises'

Vue.use(Vuetify)

const vuetify = new Vuetify({})
const store = getVuexStore()

// Input field selectors / buttons
const searchDropDown: string = '.search-bar-type-select'

/**
 * Creates and mounts a component, so that it can be tested.
 *
 * @returns a Wrapper<SearchBar> object with the given parameters.
 */
function createComponent (): Wrapper<any> {
  const localVue = createLocalVue()
  localVue.use(CompositionApi)
  localVue.use(Vuetify)
  document.body.setAttribute('data-app', 'true')
  return mount(SearchBarList, {
    localVue,
    propsData: {},
    store,
    vuetify
  })
}

describe('SearchBar component basic tests', () => {
  let wrapper: Wrapper<any>

  beforeEach(async () => {
    await store.dispatch('setUserInfo', {
      firstname: 'test',
      lastname: 'tester',
      username: 'user',
      settings: mockedDisableAllUserSettingsResponse
    })
    resetLDMocks()
    wrapper = createComponent()
  })
  afterEach(() => {
    wrapper.destroy()
  })

  it('renders SearchBar Component with basic elements', async () => {
    expect(wrapper.findComponent(SearchBarList).exists()).toBe(true)
    expect(wrapper.find(searchDropDown).exists()).toBe(true)
    
  })

  it('shows ppr options only', async () => {
    await store.dispatch('setAuthRoles', [])
    mockFlags({ 'bcregistry-ui-ppr-mhr-staff-only': true })
    wrapper.vm.updateSelections()
    await flushPromises
    expect(wrapper.vm.$data.displayItems.length).toBe(8)
  })

  it('hides and shows things for staff', async () => {
    await store.dispatch('setAuthRoles', ['staff', 'ppr_staff'])
    mockFlags({ 'bcregistry-ui-ppr-mhr-staff-only': true })
    wrapper.vm.updateSelections()
    await flushPromises
    expect(wrapper.vm.$data.displayItems.length).toBe(14)
  })

  it('sends selected event', async () => {
    wrapper.vm.selectSearchType(SearchTypes[1])
    expect(getLastEvent(wrapper, 'selected')).toBe(SearchTypes[1])
  })
})

