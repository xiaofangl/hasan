module.exports = {
    root: true,
    parser: 'babel-eslint',
    parserOptions: {
        sourceType: 'module'
    },
    // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
    extends: 'standard',
    // required to lint *.vue files
    plugins: [
        'html',
        'vue'
    ],
    // add your custom rules here
    'rules': {
        // "indent": [2, 4],
        "semi": 0,
        // "eol-last": 0,
        // allow paren-less arrow functions
        // 'arrow-parens': 0,
        "no-multiple-empty-lines": [1, {"max": 4}],
        'space-before-function-paren': 0,
        "no-trailing-spaces": 1,
        "camelcase": 0,
        "padded-blocks": 0,
        "handle-callback-err": 0,
        "comma-dangle": [2, "never"],
        // allow async-await
        // 'generator-star-spacing': 0,
        // allow debugger during development
        'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0
    }
}
