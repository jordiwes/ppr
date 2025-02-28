<template>
  <v-container id="registration-bar" fluid no-gutters class="registration-bar pa-0">
    <v-row no-gutters style="min-width: 345px">
      <v-col>
        <div class="actions">
          <registration-bar-type-ahead-list v-if="hasRPPR"
            :defaultLabel="labelText"
            :defaultDense="false"
            :defaultClearable="false"
            @selected="newRegistration($event)"
            />
          <registration-bar-button-list v-else @selected="newRegistration($event)"/>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, toRefs } from '@vue/composition-api'
import { useActions, useGetters } from 'vuex-composition-helpers'

import RegistrationBarButtonList from '@/components/registration/RegistrationBarButtonList.vue'
import RegistrationBarTypeAheadList from '@/components/registration/RegistrationBarTypeAheadList.vue'
import {
  AccountProductCodes, AccountProductRoles, // eslint-disable-line no-unused-vars
  APIRegistrationTypes
} from '@/enums'
import { AccountProductSubscriptionIF, RegistrationTypeIF } from '@/interfaces' // eslint-disable-line no-unused-vars

export default defineComponent({
  components: {
    RegistrationBarButtonList,
    RegistrationBarTypeAheadList
  },
  emits: ['selected-registration-type'],
  setup (props, { emit }) {
    const { getAccountProductSubscriptions } = useGetters<any>(['getAccountProductSubscriptions'])
    const { setRegistrationTypeOtherDesc } = useActions<any>(['setRegistrationTypeOtherDesc'])
    const localState = reactive({
      labelText: 'Start a new Registration (Select a type)'
    })
    const hasRPPR = computed(() => {
      const productSubscriptions = getAccountProductSubscriptions.value as AccountProductSubscriptionIF
      return (
        productSubscriptions?.[AccountProductCodes.RPPR].roles.includes(AccountProductRoles.EDIT) || false
      )
    })
    const newRegistration = (val: RegistrationTypeIF) => {
      if (val.registrationTypeAPI !== APIRegistrationTypes.OTHER) {
        setRegistrationTypeOtherDesc('')
      }
      emit('selected-registration-type', val)
    }

    return {
      hasRPPR,
      newRegistration,
      ...toRefs(localState)
    }
  }
})
</script>
