<template>
  <v-row justify="center" no-gutters>
    <v-col v-if="cancelText" cols="auto">
      <v-btn id="cancel-btn" class="outlined dialog-btn" outlined @click="proceed(false)">
        {{ cancelText }}
      </v-btn>
    </v-col>
    <v-col v-if="acceptText" :class="{ 'pl-3': cancelText }" cols="auto">
      <v-btn id="accept-btn" class="primary dialog-btn" @click="proceed(true)">
        {{ acceptText }}
      </v-btn>
    </v-col>
  </v-row>
</template>

<script lang="ts">
// external
import {
  computed,
  defineComponent,
  reactive,
  toRefs
} from '@vue/composition-api'

export default defineComponent({
  name: 'DialogButtons',
  props: {
    setAcceptText: String,
    setCancelText: String
  },
  emits: ['proceed'],
  setup (props, { emit }) {
    const localState = reactive({
      acceptText: computed(() => {
        return props.setAcceptText || ''
      }),
      cancelText: computed(() => {
        return props.setCancelText || ''
      })
    })
    const proceed = (val: boolean) => {
      emit('proceed', val)
    }

    return {
      proceed,
      ...toRefs(localState)
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/theme.scss';
#accept-btn {
  font-weight: normal;
}
</style>
