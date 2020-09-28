const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCssAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  entry: {
    index: ["@babel/polyfill", "./assets/js/index.js"],
    data: ["@babel/polyfill", "./assets/js/data.js"],
  },
  devServer: {
    contentBase: "./dist",
  },
  devtool: "inline-source-map",
  output: {
    filename: "[name].min.js",
    path: path.resolve(__dirname, "dist"),
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          // 'style-loader',
          MiniCssExtractPlugin.loader,
          "css-loader",
        ],
      },
      {
        test: /\.js$/,
        include: path.resolve(__dirname, "assets/js"),
        exclude: /(node_modules)|(dist)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
      {
        test: /\.(jpe?g|png|gif|svg|otf|ttf)$/i,
        loader: "file-loader?name=/assets/[name].[ext]",
      },
    ],
  },
  optimization: {
    minimizer: [new OptimizeCssAssetsPlugin(), new TerserPlugin()],
  },
  plugins: [
    new HtmlWebpackPlugin({
      filename: "index.html",
      template: "./templates/index.html",
      inject: false,
    }),
    new HtmlWebpackPlugin({
      filename: "data.html",
      template: "./templates/data.html",
      inject: false,
    }),
    new MiniCssExtractPlugin({ filename: "[name].min.css" }),
  ],
};
