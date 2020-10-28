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
      colors: {}
    },
  },
  variants: {},
  plugins: [],
}
