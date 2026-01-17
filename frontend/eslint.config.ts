import antfu from '@antfu/eslint-config'

export default antfu({
  rules: {
    'no-alert': 'off', // 暫時允許 alert
  },
})
