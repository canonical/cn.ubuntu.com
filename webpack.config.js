const path = require("path");

const config = {
  entry: {
    ["global-nav"]: "./static/js/global-nav.js"
  },
  output: {
    path: path.resolve(__dirname, "static/dist"),
    filename: "[name].js"
  },
  module: {
    rules: [
      {
        test: /\.js?$/,
        exclude: /(node_modules)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"]
          }
        }
      }
    ]
  }
};

module.exports = env => {
  // the env is set in package.json when calling webpack
  if (env && env.development) {
    config.devtool = "source-map";
    config.mode = "development";
  } else {
    config.mode = "production";
  }

  return config;
};
