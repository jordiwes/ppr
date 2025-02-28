<template :class="{ 'pl-15': leftOffset, 'pr-15': rightOffset }">
  <div :class="[`sticky-container-${size}`, { 'position-bottom': attachToBottom } ]">
    <fee-summary
      v-if="showFeeSummary"
      :setFeeType="feeType"
      :setRegistrationLength="registrationLength"
      :setRegistrationType="registrationType"
    />
    <buttons-stacked
      v-if="showButtons"
      class="pt-4"
      :setBackBtn="backBtn"
      :setCancelBtn="cancelBtn"
      :setSubmitBtn="submitBtn"
      @back="back()"
      @cancel="cancel()"
      @submit="submit()"
    />
    <div v-if="errMsg" class="err-msg pt-3">
      {{ errMsg }}
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  onMounted,
  reactive,
  toRefs,
  watch
} from '@vue/composition-api'
// local components
import { ButtonsStacked } from '@/components/common'
import { FeeSummary } from '@/composables/fees'
// local enums/interfaces/etc.
import { UIRegistrationTypes } from '@/enums' // eslint-disable-line no-unused-vars
import { FeeSummaryTypes } from '@/composables/fees/enums' // eslint-disable-line no-unused-vars
import { RegistrationLengthI } from '@/composables/fees/interfaces' // eslint-disable-line no-unused-vars

export default defineComponent({
  name: 'StickyContainer',
  components: {
    ButtonsStacked,
    FeeSummary
  },
  props: {
    // component options
    setErrMsg: {
      default: ''
    },
    setLeftOffset: {
      default: false
    },
    setRightOffset: {
      default: false
    },
    setShowButtons: {
      default: false
    },
    setShowFeeSummary: {
      default: false
    },
    setSize: {
      default: 3
    },
    // fee summary
    setFeeType: {
      type: String as () => FeeSummaryTypes
    },
    setRegistrationLength: {
      type: Object as () => RegistrationLengthI
    },
    setRegistrationType: {
      type: String as () => UIRegistrationTypes
    },
    // buttons
    setBackBtn: {
      default: ''
    },
    setCancelBtn: {
      default: ''
    },
    setSubmitBtn: {
      default: ''
    }
  },
  setup (props, { emit }) {
    const localState = reactive({
      attachToBottom: false,
      backBtn: props.setBackBtn,
      cancelBtn: props.setCancelBtn,
      errMsg: props.setErrMsg,
      feeType: props.setFeeType,
      leftOffset: props.setLeftOffset,
      registrationType: props.setRegistrationType,
      registrationLength: props.setRegistrationLength,
      rightOffset: props.setRightOffset,
      showButtons: props.setShowButtons,
      showFeeSummary: props.setShowFeeSummary,
      size: props.setSize,
      submitBtn: props.setSubmitBtn
    })
    onMounted(() => {
      if (window.innerHeight < 700) {
        localState.attachToBottom = true
      } else {
        localState.attachToBottom = false
      }
    })
    const back = () => {
      emit('back', true)
    }
    const cancel = () => {
      emit('cancel', true)
    }
    const submit = () => {
      emit('submit', true)
    }

    watch(() => props.setErrMsg, (val: string) => {
      localState.errMsg = val
    })

    watch(() => props.setRegistrationLength, (val: RegistrationLengthI) => {
      localState.registrationLength = val
    }, { deep: true, immediate: true })

    return {
      back,
      cancel,
      submit,
      ...toRefs(localState)
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';
.err-msg {
  color: $error;
  font-size: 0.75rem;
  text-align: center;
}
.position-bottom {
  bottom: 0px;
}
// matches cols=3
.sticky-container-3 {
  max-width: 316px;
  min-width: 200px;
  position: fixed;
  width: 25%;
}
</style>
