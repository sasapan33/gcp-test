const path = require('path');
console.log('webpack',)
module.exports = {
    entry: './app.js',
    output: {
        filename: 'app.bundle.js',
        path: path.resolve(__dirname, './'),
    },
    node: {
        fs: 'empty',
        net: 'empty'
    }
};
