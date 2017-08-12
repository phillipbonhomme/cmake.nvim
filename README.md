# CMake Neovim Python Plugin

- [Introduction](#introduction)
- [Installing](#installing)
    - [Downloading](#downloading)
    - [Configuring Vim](#configuring-vim)
    - [Python Version](#python_version)
    - [Initializing Vim with Remote Plugin](#initializing)
    - [Testing the New Plugin](#testing)
- [Development](#development)
    - [Unit Tests](#testing)
    - [Plugin Interface Changes](#changing-interface)

## <a id="introduction"></a>Introduction

As part of the changes included in Neovim there is a new plugin model where
plugins are separate processes which Neovim communicates to using the
MessagePack protocol.

Since plugins are distinct from the Neovim process, it is possible to write
plugins in many languages.

This is a minimal example of a Python plugin. When you want to create a new
Python plugin, you should be able to (and feel free to) copy this repository,
rename a couple files, include the plugin in your Vim config and see something
happen.

## <a id="installing"></a>Installing

### <a id="downloading"></a>Downloading

The intention of this repository is to make it quick and easy to start a new
plugin. It is just enough to show how to make the basics work.

```Bash
git clone --depth 1 https://github.com/jacobsimpson/nvim-example-python-plugin ~/.vim/bundle/nvim-example-python-plugin
rm -Rf ~/.vim/bundle/nvim-example-python-plugin/.git
```

### <a id="configuring-vim"></a>Configuring Vim

I use NeoBundle so this is an example of how to load this plugin in NeoBundle.

```VimL
" Required:
call neobundle#begin(expand('~/.vim/bundle/'))

    " Let NeoBundle manage NeoBundle
    " Required:
    NeoBundleFetch 'Shougo/neobundle.vim'

    " You probably have a number of other plugins listed here.

    " Add this line to make your new plugin load, assuming you haven't renamed it.
    NeoBundle 'nvim-example-python-plugin'
call neobundle#end()
```

If you use vim-plug, you can add this line to your plugin section:

```VimL
Plug 'jacobsimpson/nvim-example-python-plugin'
```

After running `:PlugInstall`, the files should appear in your `~/.config/nvim/plugged` directory (or whatever path you have configured for plugins).

### <a id="python_version"></a>Python Version

This plugin code works with Python 2. You can make it work with Python 3 by changing the `rplugin/python` directory to be `rplugin/python3`. See the [python-client remote plugin documentation](https://github.com/neovim/python-client#remote-new-style-plugins) for more information.

### <a id="initializing"></a>Initializing Vim with Remote Plugin

The next thing to do is to initialize the manifest for the Python part of the
plugin. The manifest is a cache that Vim keeps of the interface implemented by
the Python part of the plugin. The functions and commands it implements.

To initialize the manifest, execute:

```VimL
:UpdateRemotePlugins
```

**NOTE:** After initializing the manifest, you must restart neovim for the python
functions be be available.

### <a id="testing"></a>Testing the New Plugin

There is some VimL in the plugin that will print when Neovim is starting up:

    Starting the example Python Plugin

That will confirm that the VimL portions of the plugin are loading correctly.

There is a function defined in the VimL portion of the plugin which echos some
text. You can execute the function like this:

```VimL
:exec DoItVimL()
```

Now that the manifest is initialized, it should be possible to invoke the
function defined in the Python part of the plugin. Look in \_\_init\_\_ to see
the implementation.

```VimL
:exec DoItPython()
```

## <a id="development"></a>Development

On it's own, this plugin doesn't do anything interesting, so the expectation is
that you will want to modify it.

### <a id="testing"></a>Unit Tests

Run the unit tests:

```Shell
python3 -m unittest -v tests/rplugin/python3/test_cmake.py
```

