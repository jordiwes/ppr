import { Validators, createFormValidation } from '@lemoncode/fonk'
import { rangeNumber } from '@lemoncode/fonk-range-number-validator'
import { serialNumberValidator } from '@/utils/validators/serial-number.validator'

const validationSchema = {
  field: {
    type: [
      {
        validator: Validators.required.validator,
        message: 'Type is required',
        customArgs: { trim: true }
      }
    ],
    model: [
      {
        validator: Validators.required.validator,
        message: 'Enter the vehicle model',
        customArgs: { trim: true }
      }
    ],
    manufacturedHomeRegistrationNumber: [
      {
        validator: rangeNumber.validator,
        customArgs: {
          strictTypes: false,
          min: {
            value: 100000,
            inclusive: true
          },
          max: {
            value: 999999,
            inclusive: true
          }
        },
        message: 'Manufactured Home Registration Number must contain 6 digits'
      },
      {
        validator: Validators.pattern.validator,
        customArgs: { pattern: /^\d+$/ },
        message: 'Manufactured Home Registration Number must contain 6 digits'
      }
    ],
    year: [
      {
        validator: rangeNumber.validator,
        customArgs: {
          strictTypes: false,
          min: {
            value: 1800,
            inclusive: true
          },
          max: {
            value: new Date().getFullYear() + 1,
            inclusive: true
          }
        },
        message: 'Enter a valid year'
      }
    ],
    make: [
      {
        validator: Validators.required.validator,
        message: 'Enter the vehicle make',
        customArgs: { trim: true }
      }
    ]
  },
  record: {
    serialNumber: [
      {
        validator: serialNumberValidator
      }
    ]
  }
}
// @ts-ignore - there is a type mismatch in the structure above, but it still works
export const formValidation = createFormValidation(validationSchema)
