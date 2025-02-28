<template>
  <v-container flat class="pa-0">
    <v-row v-if="options.header" class="summary-header rounded-top" no-gutters>
      <v-col cols="auto" class="pa-4">
        <v-icon v-if="options.iconImage" :color="options.iconColor">{{ options.iconImage }}</v-icon>
        <label class="pl-3" :class="$style['sectionText']">
          <strong>{{ options.header }}</strong>
        </label>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-data-table
          class="party-summary-table"
          :headers="headers"
          :items="items"
          disable-pagination
          disable-sort
          hide-default-footer
          no-data-text=""
        >
          <template v-slot:item="row" class="party-data-table">
            <tr :key="row.item.id" class="party-row"
            :class="{ 'disabled-text-not-first': row.item.action === ActionTypes.REMOVED}">
              <td class="list-item__title title-text" style="padding-left:30px">
                <v-row no-gutters>
                  <v-col cols="3">
                    <div class="icon-div mt-n1 pr-4">
                      <v-icon v-if="isBusiness(row.item)">mdi-domain</v-icon>
                      <v-icon v-else>mdi-account</v-icon>
                    </div>
                  </v-col>
                  <v-col cols="9">
                    <div :class="{ 'disabled-text': row.item.action === ActionTypes.REMOVED}">
                      {{ getName(row.item) }}
                    </div>
                    <div
                      v-if="
                        row.item.action &&
                          registrationFlowType === RegistrationFlowType.AMENDMENT
                      "
                    >
                      <v-chip x-small label color="primary" text-color="white">
                        {{ row.item.action }}
                      </v-chip>
                    </div>
                  </v-col>
                </v-row>
              </td>
              <td>
                <base-address
                  :editing="false"
                  :schema="DefaultSchema"
                  :value="row.item.address"
                />
              </td>
              <td>{{ row.item.emailAddress }}</td>
              <td v-if="options.isDebtorSummary">{{ getFormattedBirthdate(row.item) }}</td>
              <td v-else>{{ row.item.code }}</td>
            </tr>
          </template>
          <template v-if="options.enableNoDataAction" slot="no-data">
            <v-icon color="error">mdi-information-outline</v-icon>
            <span class="invalid-message">
              This step is unfinished.
            </span>
            <span class="invalid-link" @click="noDataAction()">
              Return to this step to complete it.
            </span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {
  defineComponent,
  reactive,
  computed,
  toRefs
} from '@vue/composition-api'
import { useGetters } from 'vuex-composition-helpers'

// local
import { BaseAddress } from '@/composables/address'
import { DefaultSchema } from '@/composables/address/resources'
import { useParty } from '@/composables/useParty'
import { BaseHeaderIF, PartyIF, PartySummaryOptionsI } from '@/interfaces' // eslint-disable-line no-unused-vars
import { RegistrationFlowType, ActionTypes } from '@/enums'

export default defineComponent({
  name: 'BasePartySummary',
  components: {
    BaseAddress
  },
  props: {
    setHeaders: {
      default: () => [] as Array<BaseHeaderIF>
    },
    setItems: {
      default: () => [] as Array<PartyIF>
    },
    setOptions: {
      default: () => {
        return {
          enableNoDataAction: false,
          header: '',
          iconColor: '',
          iconImage: '',
          isDebtorSummary: false,
          isRegisteringParty: false
        } as PartySummaryOptionsI
      }
    }
  },
  emits: ['triggerNoDataAction'],
  setup (props, { emit }) {
    const { getRegistrationFlowType } = useGetters<any>([
      'getRegistrationFlowType'
    ])
    const registrationFlowType = getRegistrationFlowType.value
    const localState = reactive({
      headers: props.setHeaders,
      items: computed((): PartyIF[] => {
        if ((registrationFlowType === RegistrationFlowType.AMENDMENT) && (!localState.options.isRegisteringParty)) {
          const displayArray = []
          for (let i = 0; i < props.setItems.length; i++) {
            if (props.setItems[i].action) {
              displayArray.push(props.setItems[i])
            }
          }
          return displayArray
        } else {
          return props.setItems
        }
      }),
      options: props.setOptions
    })
    const noDataAction = (): void => {
      emit('triggerNoDataAction', true)
    }
    const { getFormattedBirthdate, getName, isBusiness } = useParty()

    return {
      ...toRefs(localState),
      registrationFlowType,
      RegistrationFlowType,
      ActionTypes,
      getFormattedBirthdate,
      getName,
      isBusiness,
      noDataAction,
      DefaultSchema
    }
  }
})
</script>

<style lang="scss" module>
@import '@/assets/styles/theme.scss';
.sectionText {
  color: $gray9;
}
</style>
