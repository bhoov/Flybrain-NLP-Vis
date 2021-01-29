module.exports = {
  corePlugins: {
    preflight: false, // by default, tailwind strips all styling from an HTML document
  },
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      colors: {},
      screens: {
        "xl": "1410px"
      }
    },
  },
  variants: {},
  plugins: [],
}
