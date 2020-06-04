module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true,
    jest: true
  },
  extends: ["eslint:recommended", "plugin:prettier/recommended"],
  parserOptions: {
    sourceType: "module"
  },
  rules: {
    "prettier/prettier": "error",
    "object-curly-spacing": ["error", "always"]
  }
};
