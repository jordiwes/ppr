<template>
  <v-container fluid no-gutters class="white px-0 py-6">
    <v-row class="px-6" align="center">
      <v-col cols="6">
        <v-text-field
          filled
          label="Secured Party Code or Name"
          id="txt-code"
          v-model="searchValue"
          persistent-hint
          hint="Enter at least the first 3 characters."
          :disabled="autoCompleteDisabled"
        />
      </v-col>
      <v-col cols="6" :class="{ 'disabled-text': autoCompleteDisabled }">
        or
        <a
          id="add-party"
          class="generic-link"
          :class="{ 'disabled-text': autoCompleteDisabled }"
          @click="goToAddSecuredParty"
          :disabled="autoCompleteDisabled"
          >Add a Secured Party that doesn't have a code</a
        >
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12">
        <party-autocomplete
          :autoCompleteItems="autoCompleteResults"
          :defaultClickToAdd="false"
          :setAutoCompleteActive="setAutoCompleteActive"
          @selectItem="searchValue = ''"
        />
      </v-col>
    </v-row>
    <v-row class="px-6" align="center" v-if="registrationFlowType !== RegistrationFlowType.AMENDMENT">
      <v-col cols="auto" class="pr-0">
        <v-checkbox
          id="add-registering-party"
          class="reg-checkbox pa-0 ma-0"
          @click="addRegisteringParty"
          v-model="registeringPartySelected"
          :hide-details="true"
          :disabled="autoCompleteDisabled"
        >
        </v-checkbox>
      </v-col>
      <v-col class="pl-0" :class="{ 'disabled-text': autoCompleteDisabled }">
        Include the Registering Party as a Secured Party
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {
  defineComponent,
  reactive,
  toRefs,
  watch,
  computed
} from '@vue/composition-api'
import { useGetters } from 'vuex-composition-helpers'
import { partyCodeSearch } from '@/utils'
import { RegistrationFlowType } from '@/enums'
import { SearchPartyIF, PartyIF } from '@/interfaces' // eslint-disable-line no-unused-vars
import PartyAutocomplete from './PartyAutocomplete.vue'

export default defineComponent({
  components: {
    PartyAutocomplete
  },
  props: {
    isAutoCompleteDisabled: {
      type: Boolean,
      default: false
    },
    registeringPartyAdded: {
      type: Boolean,
      default: false
    }
  },
  emits: [
    'showSecuredPartyAdd',
    'addRegisteringParty',
    'removeRegisteringParty'
  ],
  setup (props, context) {
    const { getRegistrationFlowType } = useGetters<any>([
      'getRegistrationFlowType'
    ])
    const registrationFlowType = getRegistrationFlowType.value
    const localState = reactive({
      searchValue: '',
      autoCompleteResults: null,
      autoCompleteDisabled: computed((): boolean => {
        return props.isAutoCompleteDisabled
      }),
      setAutoCompleteActive: false,
      registeringPartySelected: false,
      resultAdded: [],
      partyCode: 0
    })

    const goToAddSecuredParty = () => {
      if (localState.searchValue) {
        localState.searchValue = ''
        localState.setAutoCompleteActive = false
        closeAutoComplete()
      }
      context.emit('showSecuredPartyAdd')
    }

    const addRegisteringParty = () => {
      if (localState.registeringPartySelected) {
        context.emit('addRegisteringParty')
      } else {
        context.emit('removeRegisteringParty')
      }
    }

    const closeAutoComplete = () => {
      localState.setAutoCompleteActive = false
      localState.autoCompleteResults = []
    }

    const updateAutoCompleteResults = async (searchValue: string) => {
      const response: [SearchPartyIF] = await partyCodeSearch(
        searchValue,
        false
      )
      // check if results are still relevant before updating list
      if (response?.length > 0) {
        // will take up to 25 results
        localState.autoCompleteResults = response?.slice(0, 25)
      } else {
        localState.autoCompleteResults = []
      }
      localState.setAutoCompleteActive = true
    }

    watch(
      () => localState.searchValue,
      (val: string) => {
        if (localState.searchValue.length >= 3) {
          updateAutoCompleteResults(val)
        }
      }
    )
    watch(
      () => props.registeringPartyAdded,
      (sel: boolean) => {
        localState.registeringPartySelected = sel
      }
    )

    return {
      goToAddSecuredParty,
      addRegisteringParty,
      closeAutoComplete,
      registrationFlowType,
      RegistrationFlowType,
      ...toRefs(localState)
    }
  }
})
</script>

<style lang="scss" module>
@import '@/assets/styles/theme.scss';

.close-btn-row {
  height: 1rem;
}
</style>
