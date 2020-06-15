# [cn.ubuntu.com](http://cn.ubuntu.com)

[![CircleCI build status](https://circleci.com/gh/canonical-web-and-design/cn.ubuntu.com.svg?style=shield)](https://circleci.com/gh/canonical-web-and-design/cn.ubuntu.com) [![Code coverage](https://codecov.io/gh/canonical-web-and-design/cn.ubuntu.com/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/cn.ubuntu.com)

A paired-down, Chinese-language version of the ubuntu.com website.

## Local development

The simplest way to run the site locally is to first [install Docker](https://docs.docker.com/engine/installation/) (on Linux you may need to [add your user to the `docker` group](https://docs.docker.com/engine/installation/linux/linux-postinstall/)), and then use the `./run` script:

``` bash
./run
```

Once the containers are setup, you can visit <http://127.0.0.1:8010> in your browser.

### Building CSS

For working on [Sass files](_sass), you may want to dynamically watch for changes to rebuild the CSS whenever something changes.

To setup the watcher, open a new terminal window and run:

``` bash
./run watch
```

# Deploy
You can find the deployment config in the deploy folder.

License
---

The content of this project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/), and the underlying code used to format and display that content is licensed under the [LGPLv3](http://opensource.org/licenses/lgpl-3.0.html) by [Canonical Ltd](http://www.canonical.com/).


With ♥ from Canonical
